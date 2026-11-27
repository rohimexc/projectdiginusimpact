import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.urls import reverse

from .models import Page, Menu, SiteSetting, SocialMedia, QuickLink
from .forms import PageForm, MenuForm, SiteSettingForm, SocialMediaForm, QuickLinkForm


def staff_required(view_func):
    """Decorator khusus untuk memastikan user adalah Super Admin"""
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('landing:login')
        if not request.user.is_superuser:
            messages.error(request, "Akses ditolak! Menu CMS & Pengaturan hanya dapat diakses oleh Super Admin.")
            return redirect('landing:dashboard_admin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==========================================
# 1. PUBLIC PAGE VIEW & PREVIEW
# ==========================================

def page_detail(request, slug):
    """
    Menampilkan halaman dinamis berdasarkan slug.
    Mendukung HTML Content, PDF Preview, External Redirect, Internal Route, dan File Download.
    """
    page = get_object_or_404(Page, slug=slug)
    is_preview = request.GET.get('preview') == '1'
    is_superuser = request.user.is_authenticated and request.user.is_superuser

    # Validasi status Draft (hanya Super Admin yang dapat melakukan preview draft)
    if page.status == 'draft' and not (is_preview and is_superuser):
        raise Http404("Halaman ini masih dalam status konsep (Draft) dan belum dipublikasikan.")

    # Redirect jika jenisnya tautan eksternal
    if page.content_type == 'external_link':
        if page.external_url:
            return redirect(page.external_url)
        raise Http404("Tautan eksternal belum ditentukan.")

    # Redirect jika jenisnya tautan internal
    if page.content_type == 'internal_link':
        if page.internal_url:
            return redirect(page.internal_url)
        raise Http404("Tautan internal belum ditentukan.")

    # Unduh berkas jika jenisnya file_download
    if page.content_type == 'file_download':
        if page.file:
            return redirect(page.file.url)
        raise Http404("Berkas unduhan belum diunggah.")

    # Jika dropdown only, arahkan ke beranda
    if page.content_type == 'dropdown':
        return redirect('landing:landing_home')

    # Cari menu terkait untuk breadcrumbs (jika ada)
    related_menu = Menu.objects.filter(page=page).select_related('parent').first()

    context = {
        'page': page,
        'is_preview': is_preview and is_superuser,
        'is_staff': is_superuser,
        'related_menu': related_menu,
    }
    return render(request, 'cms/page_detail.html', context)


# ==========================================
# 2. DASHBOARD CMS - KELOLA MENU
# ==========================================

@login_required
@staff_required
def dashboard_menu_list(request):
    """Daftar manajemen menu navigasi"""
    # Ambil menu dengan struktur hierarki
    all_menus = list(Menu.objects.all().select_related('page', 'parent').order_by('order', 'id'))
    
    menu_dict = {}
    root_menus = []
    
    for m in all_menus:
        m.submenus = []
        menu_dict[m.id] = m
        
    for m in menu_dict.values():
        if m.parent_id and m.parent_id in menu_dict:
            menu_dict[m.parent_id].submenus.append(m)
        elif not m.parent_id:
            root_menus.append(m)

    context = {
        'root_menus': root_menus,
        'total_menus': len(all_menus),
    }
    return render(request, 'cms/admin/menu_list.html', context)


@login_required
@staff_required
def dashboard_menu_create(request):
    """Tambah menu baru"""
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save()
            messages.success(request, f"Menu '{menu.title}' berhasil ditambahkan.")
            return redirect('cms:dashboard_menu_list')
    else:
        # Pre-fill parent jika dipilih dari daftar
        initial = {}
        parent_id = request.GET.get('parent')
        if parent_id:
            initial['parent'] = parent_id
        form = MenuForm(initial=initial)

    return render(request, 'cms/admin/menu_form.html', {'form': form, 'title': 'Tambah Menu Baru'})


@login_required
@staff_required
def dashboard_menu_edit(request, pk):
    """Ubah menu navigasi"""
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            form.save()
            messages.success(request, f"Menu '{menu.title}' berhasil diperbarui.")
            return redirect('cms:dashboard_menu_list')
    else:
        form = MenuForm(instance=menu)

    return render(request, 'cms/admin/menu_form.html', {'form': form, 'menu': menu, 'title': f"Ubah Menu: {menu.title}"})


@login_required
@staff_required
def dashboard_menu_delete(request, pk):
    """Hapus menu navigasi"""
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        title = menu.title
        menu.delete()
        messages.success(request, f"Menu '{title}' dan submenunya berhasil dihapus.")
        return redirect('cms:dashboard_menu_list')
    return render(request, 'cms/admin/confirm_delete.html', {'object': menu, 'type': 'Menu Navigasi'})


@login_required
@staff_required
@require_POST
def dashboard_menu_reorder(request):
    """Endpoint AJAX untuk drag & drop ordering menu"""
    try:
        data = json.loads(request.body)
        order_list = data.get('order', [])  # list of id: order
        for idx, item_id in enumerate(order_list, start=1):
            Menu.objects.filter(id=item_id).update(order=idx)
        return JsonResponse({'status': 'success', 'message': 'Urutan menu berhasil disimpan.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# ==========================================
# 3. DASHBOARD CMS - KELOLA HALAMAN
# ==========================================

@login_required
@staff_required
def dashboard_page_list(request):
    """Daftar manajemen halaman dinamis"""
    pages = Page.objects.all().order_by('-updated_at')
    
    # Filter status dan tipe konten jika ada
    status_filter = request.GET.get('status')
    type_filter = request.GET.get('type')
    q = request.GET.get('q')

    if status_filter:
        pages = pages.filter(status=status_filter)
    if type_filter:
        pages = pages.filter(content_type=type_filter)
    if q:
        pages = pages.filter(title__icontains=q)

    context = {
        'pages': pages,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'search_query': q or '',
    }
    return render(request, 'cms/admin/page_list.html', context)


@login_required
@staff_required
def dashboard_page_create(request):
    """Buat halaman dinamis baru"""
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save()
            messages.success(request, f"Halaman '{page.title}' berhasil dibuat.")
            return redirect('cms:dashboard_page_list')
    else:
        form = PageForm()

    return render(request, 'cms/admin/page_form.html', {'form': form, 'title': 'Buat Halaman Baru'})


@login_required
@staff_required
def dashboard_page_edit(request, pk):
    """Ubah halaman dinamis"""
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, f"Halaman '{page.title}' berhasil diperbarui.")
            return redirect('cms:dashboard_page_list')
    else:
        form = PageForm(instance=page)

    return render(request, 'cms/admin/page_form.html', {'form': form, 'page': page, 'title': f"Ubah Halaman: {page.title}"})


@login_required
@staff_required
def dashboard_page_delete(request, pk):
    """Hapus halaman dinamis"""
    page = get_object_or_404(Page, pk=pk)
    if request.method == 'POST':
        title = page.title
        page.delete()
        messages.success(request, f"Halaman '{title}' berhasil dihapus.")
        return redirect('cms:dashboard_page_list')
    return render(request, 'cms/admin/confirm_delete.html', {'object': page, 'type': 'Halaman CMS'})


# ==========================================
# 4. DASHBOARD CMS - SITE SETTINGS
# ==========================================

@login_required
@staff_required
def dashboard_site_settings(request):
    """
    Manajemen Pengaturan Situs (Site Settings)
    Mencakup 4 Tab: Identitas & Logo, Footer, Kontak & Sosmed, dan Tautan Cepat.
    """
    settings_obj = SiteSetting.get_solo()
    active_tab = request.GET.get('tab', 'identitas')

    if request.method == 'POST' and 'save_settings' in request.POST:
        form = SiteSettingForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Pengaturan identitas dan kontak situs berhasil disimpan.")
            return redirect(reverse('cms:dashboard_site_settings') + f"?tab={request.POST.get('current_tab', 'identitas')}")
    else:
        form = SiteSettingForm(instance=settings_obj)

    social_list = settings_obj.social_media_list.all().order_by('order', 'id')
    quick_links = settings_obj.quick_links.all().order_by('order', 'id')

    context = {
        'settings_obj': settings_obj,
        'form': form,
        'social_list': social_list,
        'quick_links': quick_links,
        'active_tab': active_tab,
        'social_form': SocialMediaForm(),
        'quicklink_form': QuickLinkForm(),
    }
    return render(request, 'cms/admin/site_settings.html', context)


@login_required
@staff_required
def dashboard_social_create(request):
    """Tambah akun sosial media"""
    settings_obj = SiteSetting.get_solo()
    if request.method == 'POST':
        form = SocialMediaForm(request.POST)
        if form.is_valid():
            social = form.save(commit=False)
            social.setting = settings_obj
            social.save()
            messages.success(request, f"Sosial media {social.get_platform_display()} berhasil ditambahkan.")
    return redirect(reverse('cms:dashboard_site_settings') + '?tab=sosmed')


@login_required
@staff_required
def dashboard_social_delete(request, pk):
    """Hapus akun sosial media"""
    social = get_object_or_404(SocialMedia, pk=pk)
    if request.method == 'POST':
        social.delete()
        messages.success(request, "Sosial media berhasil dihapus.")
    return redirect(reverse('cms:dashboard_site_settings') + '?tab=sosmed')


@login_required
@staff_required
def dashboard_quicklink_create(request):
    """Tambah tautan cepat footer"""
    settings_obj = SiteSetting.get_solo()
    if request.method == 'POST':
        form = QuickLinkForm(request.POST, request.FILES)
        if form.is_valid():
            link = form.save(commit=False)
            link.setting = settings_obj
            link.save()
            messages.success(request, f"Tautan cepat '{link.title}' berhasil ditambahkan.")
    return redirect(reverse('cms:dashboard_site_settings') + '?tab=tautan')


@login_required
@staff_required
def dashboard_quicklink_delete(request, pk):
    """Hapus tautan cepat footer"""
    link = get_object_or_404(QuickLink, pk=pk)
    if request.method == 'POST':
        link.delete()
        messages.success(request, "Tautan cepat berhasil dihapus.")
    return redirect(reverse('cms:dashboard_site_settings') + '?tab=tautan')

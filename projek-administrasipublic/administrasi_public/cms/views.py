import json
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Page, Menu


def page_detail(request, slug):
    """
    Menampilkan halaman CMS dinamis berdasarkan slug URL.
    Mendukung mode Preview (hanya untuk staf jika status halaman Draft).
    """
    is_preview = (request.GET.get('preview') == '1' and (request.user.is_staff or request.user.is_superuser))
    
    if is_preview:
        page = get_object_or_404(Page, slug=slug)
    else:
        # Pengunjung umum hanya dapat mengakses halaman Published
        page = get_object_or_404(Page, slug=slug, status='published')

    # Tangani jenis konten
    if page.content_type == 'external_link':
        if page.external_url:
            return redirect(page.external_url)
        raise Http404("Tautan eksternal tidak ditemukan.")

    elif page.content_type == 'internal_link':
        if page.internal_url:
            return redirect(page.internal_url)
        raise Http404("Tautan internal tidak ditemukan.")

    elif page.content_type == 'file_download':
        if page.file_download:
            return FileResponse(
                page.file_download.open('rb'),
                as_attachment=True,
                filename=os.path.basename(page.file_download.name)
            )
        raise Http404("Berkas unduhan tidak ditemukan.")

    elif page.content_type == 'dropdown_only':
        return redirect('home')

    elif page.content_type == 'pdf':
        context = {
            'page': page,
            'is_preview': is_preview,
        }
        return render(request, 'cms/page_pdf.html', context)

    else:
        # Default: HTML Content
        context = {
            'page': page,
            'is_preview': is_preview,
        }
        return render(request, 'cms/page_detail.html', context)


@login_required(login_url='user_login')
@require_POST
def reorder_menus(request):
    """
    Endpoint AJAX untuk Drag and Drop Menu Ordering dari Django Admin.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'status': 'error', 'message': 'Akses ditolak.'}, status=403)

    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        for item in items:
            menu_id = item.get('id')
            order = item.get('order')
            if menu_id is not None and order is not None:
                Menu.objects.filter(id=menu_id).update(order=order)
        return JsonResponse({'status': 'success', 'message': 'Urutan menu berhasil diperbarui!'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

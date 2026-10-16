from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Sambutan, Galeri, Berita, TenagaPendidik
from .forms import BeritaForm, TenagaPendidikForm
from django.contrib.auth.decorators import login_required
# ==========================================
# 1. LANDING PAGE & BERITA
# ==========================================

# View Halaman Utama (Landing Page)
def home(request):
    sambutan = Sambutan.objects.first()
    daftar_galeri = Galeri.objects.all()[:6]
    daftar_berita = Berita.objects.all().order_by('-posted_at')[:3]
    # Ambil 3 tenaga kependidikan untuk dipaparkan di seksyen Laman Utama
    daftar_tenaga_kependidikan = TenagaPendidik.objects.all()[:3]

    context = {
        'sambutan': sambutan,
        'daftar_galeri': daftar_galeri,
        'daftar_berita': daftar_berita,
        'daftar_tenaga_kependidikan': daftar_tenaga_kependidikan,
    }
    return render(request, 'core/index.html', context)


# View Senarai Semua Berita (Carian, Penapis, Penomboran Halaman)
def berita_list(request):
    query = request.GET.get('q', '')
    tahun = request.GET.get('tahun', '')
    bulan = request.GET.get('bulan', '')
    tanggal = request.GET.get('tanggal', '')

    berita_qs = Berita.objects.all().order_by('-posted_at')

    if query:
        berita_qs = berita_qs.filter(
            Q(judul__icontains=query) | Q(konten__icontains=query) | Q(ringkasan__icontains=query)
        )

    if tahun:
        berita_qs = berita_qs.filter(posted_at__year=tahun)
    if bulan:
        berita_qs = berita_qs.filter(posted_at__month=bulan)
    if tanggal:
        berita_qs = berita_qs.filter(posted_at__date=tanggal)

    paginator = Paginator(berita_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_tahun': tahun,
        'selected_bulan': bulan,
        'selected_tanggal': tanggal,
    }
    return render(request, 'core/Berita/list.html', context)


# View Terperinci Berita
def berita_detail(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    berita_terkait = Berita.objects.exclude(pk=pk).order_by('-posted_at')[:3]
    return render(request, 'core/Berita/detail.html', {'berita': berita, 'berita_terkait': berita_terkait})


# View Tambah Berita (Create)
def berita_create(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('berita_list')
    else:
        form = BeritaForm()
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Tambah Berita Baru'})


# View Kemas Kini Berita (Update)
def berita_update(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES, instance=berita)
        if form.is_valid():
            form.save()
            return redirect('berita_detail', pk=berita.pk)
    else:
        form = BeritaForm(instance=berita)
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Edit Berita'})


# View Padam Berita (Delete)
def berita_delete(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        berita.delete()
        return redirect('berita_list')
    return render(request, 'core/Berita/delete_confirm.html', {'berita': berita})


# ==========================================
# 2. TENAGA KEPENDIDIKAN
# ==========================================

# View Halaman Katalog Tenaga Kependidikan
def tenaga_kependidikan_list(request):
    query = request.GET.get('q', '')
    kependidikan_qs = TenagaPendidik.objects.all().order_by('nama')

    if query:
        kependidikan_qs = kependidikan_qs.filter(
            Q(nama__icontains=query) |
            Q(bidang_ilmu__icontains=query) |
            Q(nidn__icontains=query)
        )

    context = {
        'tenaga_kependidikan_list': kependidikan_qs,
        'query': query,
    }
    return render(request, 'core/kependidikan/list.html', context)


# View Terperinci Tenaga Kependidikan
def tenaga_kependidikan_detail(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    tenaga_kependidikan_lainnya = TenagaPendidik.objects.exclude(pk=pk)[:3]
    context = {
        'tenaga_kependidikan': tenaga_kependidikan,
        'tenaga_kependidikan_lainnya': tenaga_kependidikan_lainnya,
    }
    return render(request, 'core/kependidikan/detail.html', context)


# View Tambah Tenaga Kependidikan (Create)
def tenaga_kependidikan_create(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tenaga_kependidikan_list')
    else:
        form = TenagaPendidikForm()
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Tambah Tenaga Kependidikan'})


# View Kemas Kini Tenaga Kependidikan (Update)
def tenaga_kependidikan_update(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=tenaga_kependidikan)
        if form.is_valid():
            form.save()
            return redirect('tenaga_kependidikan_list')
    else:
        form = TenagaPendidikForm(instance=tenaga_kependidikan)
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Edit Tenaga Kependidikan'})


# View Padam Tenaga Kependidikan (Delete)
def tenaga_kependidikan_delete(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        tenaga_kependidikan.delete()
        return redirect('tenaga_kependidikan_list')
    return render(request, 'core/kependidikan/delete_confirm.html', {'tenaga_kependidikan': tenaga_kependidikan})


# ==========================================
# 3. AUTENTIKASI MENGGUNAKAN EMAIL / GMAIL
# ==========================================

# View Log Masuk Khusus Email & Semakan Peranan Admin
def user_login(request):
    User = get_user_model()

    # Jika sudah log masuk dan merupakan admin
    if request.user.is_authenticated:
        user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
        if user_role == 'admin' or request.user.is_staff or request.user.is_superuser:
            return redirect('/admin/')
        logout(request)
        messages.error(request, 'Akses ditolak! Akaun anda bukan Administrator.')
        return redirect('user_login')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email dan kata laluan wajib diisi.')
            return render(request, 'core/login.html')

        # 1. Cari pengguna mengikut alamat Email / Gmail
        user_obj = User.objects.filter(email__iexact=email).first()

        user = None
        if user_obj:
            user = authenticate(request, username=user_obj.get_username(), password=password)
        else:
            user = authenticate(request, username=email, password=password)

        if user is not None:
            # 2. Semak peranan (mesti role admin atau is_staff/superuser)
            user_role = getattr(user, 'role', '').lower() if hasattr(user, 'role') and user.role else ''
            if user_role == 'admin' or user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Akses ditolak! Hanya akaun dengan role Admin dibenarkan masuk ke Dashboard.')
                return redirect('user_login')
        else:
            messages.error(request, 'Email atau kata laluan yang dimasukkan salah.')

    return render(request, 'core/login.html')


# View Logout
def user_logout(request):
    logout(request)
    messages.success(request, 'Anda telah berhasil keluar (logout).')
    return redirect('user_login')

# ==========================================
# 4. CUSTOM DASHBOARD ADMIN
# ==========================================

@login_required(login_url='user_login')
def admin_dashboard(request):
    # Cek apakah user adalah admin
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not (user_role == 'admin' or request.user.is_staff or request.user.is_superuser):
        logout(request)
        messages.error(request, 'Akses ditolak! Anda bukan Administrator.')
        return redirect('user_login')

    total_berita = Berita.objects.count()
    total_tendik = TenagaPendidik.objects.count()
    daftar_berita = Berita.objects.all().order_by('-posted_at')[:5]
    daftar_tendik = TenagaPendidik.objects.all().order_by('-id')[:5]

    context = {
        'total_berita': total_berita,
        'total_tendik': total_tendik,
        'daftar_berita': daftar_berita,
        'daftar_tendik': daftar_tendik,
    }
    return render(request, 'core/admin/dashboard.html', context)

@login_required(login_url='user_login')
def admin_kelola_berita(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not (user_role == 'admin' or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    daftar_berita = Berita.objects.all().order_by('-posted_at')
    return render(request, 'core/admin/berita_kelola.html', {'daftar_berita': daftar_berita})
def berita_create(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_kelola_berita')  # <-- dialihkan kembali ke kelola berita admin
    else:
        form = BeritaForm()
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Tambah Berita Baru'})
def berita_update(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES, instance=berita)
        if form.is_valid():
            form.save()
            return redirect('admin_kelola_berita')  # <-- dialihkan kembali ke kelola berita admin
    else:
        form = BeritaForm(instance=berita)
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Edit Berita'})

# View Hapus Berita (Delete)
def berita_delete(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        berita.delete()
        messages.success(request, 'Berita berhasil dihapus!')
        return redirect('admin_kelola_berita')  # <-- Dialihkan kembali ke dashboard kelola berita
    return render(request, 'core/Berita/delete_confirm.html', {'berita': berita})

@login_required(login_url='user_login')
def admin_kelola_tendik(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not (user_role == 'admin' or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    # Mengambil semua data tendik
    daftar_tendik = TenagaPendidik.objects.all().order_by('-id')
    return render(request, 'core/admin/tendik_kelola.html', {'daftar_tendik': daftar_tendik})

# View Tambah Tenaga Kependidikan (Create)
def tenaga_kependidikan_create(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_kelola_tendik')  # <-- Kembali ke dashboard kelola tendik
    else:
        form = TenagaPendidikForm()
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Tambah Tenaga Kependidikan'})


# View Edit Tenaga Kependidikan (Update)
def tenaga_kependidikan_update(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=tenaga_kependidikan)
        if form.is_valid():
            form.save()
            return redirect('admin_kelola_tendik')  # <-- Kembali ke dashboard kelola tendik
    else:
        form = TenagaPendidikForm(instance=tenaga_kependidikan)
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Edit Tenaga Kependidikan'})

# View Hapus Tenaga Kependidikan (Delete)
def tenaga_kependidikan_delete(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        tenaga_kependidikan.delete()
        messages.success(request, 'Data tenaga kependidikan berhasil dihapus!')
        return redirect('admin_kelola_tendik')  # <-- Dialihkan kembali ke dashboard kelola tendik
    return render(request, 'core/kependidikan/delete_confirm.html', {'tenaga_kependidikan': tenaga_kependidikan})
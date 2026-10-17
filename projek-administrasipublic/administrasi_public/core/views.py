from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Sambutan, Galeri, Berita, TenagaPendidik, AuditLog
from .forms import BeritaForm, TenagaPendidikForm

User = get_user_model()

# Fungsi Bantu Pencatatan Audit Log
def catat_audit(request, action, description):
    ip = request.META.get('REMOTE_ADDR')
    AuditLog.objects.create(
        user=request.user if request.user.is_authenticated else None,
        action=action,
        description=description,
        ip_address=ip
    )

# ==========================================
# 1. LANDING PAGE & BERITA PUBLIK
# ==========================================

def home(request):
    sambutan = Sambutan.objects.first()
    daftar_galeri = Galeri.objects.all()[:6]
    daftar_berita = Berita.objects.all().order_by('-posted_at')[:3]
    daftar_tenaga_kependidikan = TenagaPendidik.objects.filter(jenis='TENDIK')[:4]

    context = {
        'sambutan': sambutan,
        'daftar_galeri': daftar_galeri,
        'daftar_berita': daftar_berita,
        'daftar_tenaga_kependidikan': daftar_tenaga_kependidikan,
    }
    return render(request, 'core/index.html', context)


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


def berita_detail(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    berita_terkait = Berita.objects.exclude(pk=pk).order_by('-posted_at')[:3]
    return render(request, 'core/Berita/detail.html', {'berita': berita, 'berita_terkait': berita_terkait})


def tenaga_pendidik_list(request):
    query = request.GET.get('q', '')
    dosen_qs = TenagaPendidik.objects.filter(jenis='DOSEN').order_by('nama')

    if query:
        dosen_qs = dosen_qs.filter(
            Q(nama__icontains=query) |
            Q(bidang_ilmu__icontains=query) |
            Q(nidn__icontains=query)
        )

    return render(request, 'core/dosen/list.html', {'dosen_list': dosen_qs, 'query': query})


def tenaga_kependidikan_list(request):
    query = request.GET.get('q', '')
    kependidikan_qs = TenagaPendidik.objects.filter(jenis='TENDIK').order_by('nama')

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


def tenaga_kependidikan_detail(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    return render(request, 'core/kependidikan/detail.html', {'tenaga_kependidikan': tenaga_kependidikan})


# ==========================================
# 2. AUTENTIKASI (EMAIL / GMAIL)
# ==========================================

def user_login(request):
    if request.user.is_authenticated:
        user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
        if user_role == 'admin' or request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        logout(request)
        messages.error(request, 'Akses ditolak! Akun Anda bukan Administrator.')
        return redirect('user_login')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email or not password:
            messages.error(request, 'Email dan kata sandi wajib diisi.')
            return render(request, 'core/login.html')

        user_obj = User.objects.filter(email__iexact=email).first()
        user = authenticate(request, username=user_obj.get_username() if user_obj else email, password=password)

        if user is not None:
            user_role = getattr(user, 'role', '').lower() if hasattr(user, 'role') and user.role else ''
            if user_role == 'admin' or user.is_staff or user.is_superuser:
                login(request, user)
                catat_audit(request, 'Login Berhasil', f"User {user.email} masuk ke sistem.")
                messages.success(request, f"Selamat datang, {user.username}!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Akses ditolak! Hanya akun dengan role Admin yang diizinkan masuk ke Dashboard.')
                return redirect('user_login')
        else:
            messages.error(request, 'Email atau kata sandi yang dimasukkan salah.')

    return render(request, 'core/login.html')


def user_logout(request):
    if request.user.is_authenticated:
        catat_audit(request, 'Logout', f"User {request.user.email} keluar.")
    logout(request)
    messages.success(request, 'Anda telah berhasil keluar (logout).')
    return redirect('user_login')


# ==========================================
# 3. CUSTOM DASHBOARD ADMIN & SUB-MANAJEMEN
# ==========================================

@login_required(login_url='user_login')
def admin_dashboard(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not (user_role == 'admin' or request.user.is_staff or request.user.is_superuser):
        logout(request)
        messages.error(request, 'Akses ditolak! Anda bukan Administrator.')
        return redirect('user_login')

    total_berita = Berita.objects.count()
    total_dosen = TenagaPendidik.objects.filter(jenis='DOSEN').count()
    total_tendik = TenagaPendidik.objects.filter(jenis='TENDIK').count()
    total_user = User.objects.count()
    logs = AuditLog.objects.all()[:8]

    context = {
        'total_berita': total_berita,
        'total_dosen': total_dosen,
        'total_tendik': total_tendik,
        'total_user': total_user,
        'logs': logs,
    }
    return render(request, 'core/admin/dashboard.html', context)


@login_required(login_url='user_login')
def admin_kelola_berita(request):
    daftar_berita = Berita.objects.all().order_by('-posted_at')
    return render(request, 'core/admin/berita_kelola.html', {'daftar_berita': daftar_berita})


@login_required(login_url='user_login')
def admin_kelola_dosen(request):
    daftar_dosen = TenagaPendidik.objects.filter(jenis='DOSEN').order_by('-id')
    return render(request, 'core/admin/dosen_kelola.html', {'daftar_dosen': daftar_dosen})


@login_required(login_url='user_login')
def admin_kelola_tendik(request):
    daftar_tendik = TenagaPendidik.objects.filter(jenis='TENDIK').order_by('-id')
    return render(request, 'core/admin/tendik_kelola.html', {'daftar_tendik': daftar_tendik})


@login_required(login_url='user_login')
def admin_kelola_user(request):
    daftar_user = User.objects.all().order_by('-date_joined')
    return render(request, 'core/admin/user_kelola.html', {'daftar_user': daftar_user})


@login_required(login_url='user_login')
def user_toggle_status(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    target_user.is_active = not target_user.is_active
    target_user.save()
    status_str = "diaktifkan" if target_user.is_active else "dinonaktifkan"
    catat_audit(request, 'Ubah Status User', f"Akun {target_user.email} {status_str}.")
    messages.success(request, f"Akun {target_user.username} berhasil {status_str}!")
    return redirect('admin_kelola_user')


# ==========================================
# 4. CRUD OPERATIONS (BERITA & PEGAWAI)
# ==========================================

@login_required(login_url='user_login')
def berita_create(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES)
        if form.is_valid():
            b = form.save()
            catat_audit(request, 'Tambah Berita', f"Menambahkan berita: {b.judul}")
            messages.success(request, 'Berita berhasil ditambahkan!')
            return redirect('admin_kelola_berita')
    else:
        form = BeritaForm()
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Tambah Berita Baru'})


@login_required(login_url='user_login')
def berita_update(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES, instance=berita)
        if form.is_valid():
            form.save()
            catat_audit(request, 'Edit Berita', f"Memperbarui berita: {berita.judul}")
            messages.success(request, 'Berita berhasil diperbarui!')
            return redirect('admin_kelola_berita')
    else:
        form = BeritaForm(instance=berita)
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Edit Berita'})


@login_required(login_url='user_login')
def berita_delete(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        judul = berita.judul
        berita.delete()
        catat_audit(request, 'Hapus Berita', f"Menghapus berita: {judul}")
        messages.success(request, 'Berita berhasil dihapus!')
        return redirect('admin_kelola_berita')
    return render(request, 'core/Berita/delete_confirm.html', {'berita': berita})


@login_required(login_url='user_login')
def tenaga_kependidikan_create(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            t = form.save()
            target = 'admin_kelola_tendik' if t.jenis == 'TENDIK' else 'admin_kelola_dosen'
            catat_audit(request, 'Tambah Pegawai', f"Menambahkan {t.jenis}: {t.nama}")
            messages.success(request, f"Data {t.nama} berhasil ditambahkan!")
            return redirect(target)
    else:
        form = TenagaPendidikForm()
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Tambah Data Pegawai'})


@login_required(login_url='user_login')
def tenaga_kependidikan_update(request, pk):
    pegawai = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=pegawai)
        if form.is_valid():
            t = form.save()
            target = 'admin_kelola_tendik' if t.jenis == 'TENDIK' else 'admin_kelola_dosen'
            catat_audit(request, 'Edit Pegawai', f"Memperbarui {t.jenis}: {t.nama}")
            messages.success(request, f"Data {t.nama} berhasil diperbarui!")
            return redirect(target)
    else:
        form = TenagaPendidikForm(instance=pegawai)
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Edit Data Pegawai'})


@login_required(login_url='user_login')
def tenaga_kependidikan_delete(request, pk):
    pegawai = get_object_or_404(TenagaPendidik, pk=pk)
    target = 'admin_kelola_tendik' if pegawai.jenis == 'TENDIK' else 'admin_kelola_dosen'
    if request.method == 'POST':
        nama = pegawai.nama
        pegawai.delete()
        catat_audit(request, 'Hapus Pegawai', f"Menghapus pegawai: {nama}")
        messages.success(request, f"Data {nama} berhasil dihapus!")
        return redirect(target)
    return render(request, 'core/kependidikan/delete_confirm.html', {'tenaga_kependidikan': pegawai, 'back_url': target})
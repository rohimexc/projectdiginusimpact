from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Sambutan, Galeri, Berita, TenagaPendidik, AuditLog, HalamanTentang, VisiMisiTujuan, MisiItem, TujuanItem, HalamanAkademik, DokumenAkademik
from .forms import BeritaForm, TenagaPendidikForm, UserForm, SambutanForm, HalamanTentangForm, HalamanAkademikForm

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

    visi_obj = VisiMisiTujuan.objects.first()
    daftar_misi = visi_obj.misi_items.all() if visi_obj else []
    daftar_tujuan = visi_obj.tujuan_items.all() if visi_obj else []

    context = {
        'sambutan': sambutan,
        'daftar_galeri': daftar_galeri,
        'daftar_berita': daftar_berita,
        'daftar_tenaga_kependidikan': daftar_tenaga_kependidikan,
        'visi_obj': visi_obj,
        'daftar_misi': daftar_misi,
        'daftar_tujuan': daftar_tujuan,
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
            Q(judul__icontains=query) | Q(konten__icontains=query)
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
        if 'admin' in user_role or request.user.is_staff or request.user.is_superuser:
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
            if 'admin' in user_role or user.is_staff or user.is_superuser:
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
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        messages.error(request, 'Akses ditolak! Anda bukan Administrator.')
        return redirect('user_login')

    total_berita = Berita.objects.count()

    dosen_qs = TenagaPendidik.objects.filter(jenis='DOSEN')
    total_dosen = dosen_qs.count()
    dosen_l = dosen_qs.filter(jenis_kelamin='L').count()
    dosen_p = dosen_qs.filter(jenis_kelamin='P').count()

    tendik_qs = TenagaPendidik.objects.filter(jenis='TENDIK')
    total_tendik = tendik_qs.count()
    tendik_l = tendik_qs.filter(jenis_kelamin='L').count()
    tendik_p = tendik_qs.filter(jenis_kelamin='P').count()

    total_user = User.objects.count()
    logs = AuditLog.objects.all().order_by('-timestamp')

    context = {
        'total_berita': total_berita,
        'total_dosen': total_dosen,
        'dosen_l': dosen_l,
        'dosen_p': dosen_p,
        'total_tendik': total_tendik,
        'tendik_l': tendik_l,
        'tendik_p': tendik_p,
        'total_user': total_user,
        'logs': logs,
    }
    return render(request, 'core/admin/dashboard.html', context)


@login_required(login_url='user_login')
def admin_kelola_berita(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')
    daftar_berita = Berita.objects.all().order_by('-posted_at')
    return render(request, 'core/admin/berita_kelola.html', {'daftar_berita': daftar_berita})


@login_required(login_url='user_login')
def admin_kelola_dosen(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')
    daftar_dosen = TenagaPendidik.objects.filter(jenis='DOSEN').order_by('-id')
    return render(request, 'core/admin/dosen_kelola.html', {'daftar_dosen': daftar_dosen})


@login_required(login_url='user_login')
def admin_kelola_tendik(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')
    daftar_tendik = TenagaPendidik.objects.filter(jenis='TENDIK').order_by('-id')
    return render(request, 'core/admin/tendik_kelola.html', {'daftar_tendik': daftar_tendik})


@login_required(login_url='user_login')
def admin_kelola_user(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        messages.error(request, 'Akses ditolak! Hanya Administrator yang boleh mengakses.')
        return redirect('user_login')

    daftar_user = User.objects.all().order_by('-date_joined')
    roles_list = User.objects.values_list('role', flat=True).distinct()
    roles_list = [r for r in roles_list if r]

    context = {
        'daftar_user': daftar_user,
        'roles_list': roles_list,
    }
    return render(request, 'core/admin/user_kelola.html', context)


@login_required(login_url='user_login')
def user_toggle_status(request, pk):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    target_user = get_object_or_404(User, pk=pk)
    status_sekarang = target_user.is_active

    if status_sekarang:
        target_user.is_active = False
        target_user.save()
        catat_audit(request, 'Ubah Status User', f"Akun {target_user.email} dinonaktifkan.")
        messages.success(request, f"Akun {target_user.username} berhasil dinonaktifkan!")
    else:
        target_user.is_active = True
        target_user.save()
        catat_audit(request, 'Ubah Status User', f"Akun {target_user.email} diaktifkan.")
        messages.success(request, f"Akun {target_user.username} berhasil diaktifkan!")

    return redirect('admin_kelola_user')


# ==========================================
# 4. CRUD OPERATIONS (BERITA)
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
    judul = berita.judul
    berita.delete()
    catat_audit(request, 'Hapus Berita', f"Menghapus berita: {judul}")
    messages.success(request, 'Berita berhasil dihapus!')
    return redirect('admin_kelola_berita')


# ==========================================
# 5. CRUD KHUSUS DOSEN
# ==========================================

@login_required(login_url='user_login')
def dosen_create(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            pegawai = form.save(commit=False)
            pegawai.jenis = 'DOSEN'
            pegawai.save()
            catat_audit(request, 'Tambah Dosen', f"Menambahkan Dosen: {pegawai.nama}")
            messages.success(request, f"Data dosen {pegawai.nama} berhasil ditambahkan!")
            return redirect('admin_kelola_dosen')
    else:
        form = TenagaPendidikForm(initial={'jenis': 'DOSEN'})
    return render(request, 'core/admin/dosen_form.html', {'form': form, 'title': 'Tambah Dosen Baru'})


@login_required(login_url='user_login')
def dosen_update(request, pk):
    dosen = get_object_or_404(TenagaPendidik, pk=pk, jenis='DOSEN')
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=dosen)
        if form.is_valid():
            form.save()
            catat_audit(request, 'Edit Dosen', f"Memperbarui Dosen: {dosen.nama}")
            messages.success(request, f"Data dosen {dosen.nama} berhasil diperbarui!")
            return redirect('admin_kelola_dosen')
    else:
        form = TenagaPendidikForm(instance=dosen)
    return render(request, 'core/admin/dosen_form.html', {'form': form, 'title': f'Edit Dosen: {dosen.nama}'})


@login_required(login_url='user_login')
def dosen_delete(request, pk):
    dosen = get_object_or_404(TenagaPendidik, pk=pk, jenis='DOSEN')
    nama = dosen.nama
    dosen.delete()
    catat_audit(request, 'Hapus Dosen', f"Menghapus Dosen: {nama}")
    messages.success(request, f"Data dosen {nama} berhasil dihapus!")
    return redirect('admin_kelola_dosen')


# ==========================================
# 6. CRUD KHUSUS TENDIK
# ==========================================

@login_required(login_url='user_login')
def tendik_create(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            pegawai = form.save(commit=False)
            pegawai.jenis = 'TENDIK'
            pegawai.save()
            catat_audit(request, 'Tambah Tendik', f"Menambahkan Tendik: {pegawai.nama}")
            messages.success(request, f"Data tendik {pegawai.nama} berhasil ditambahkan!")
            return redirect('admin_kelola_tendik')
    else:
        form = TenagaPendidikForm(initial={'jenis': 'TENDIK'})
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Tambah Tendik Baru'})


@login_required(login_url='user_login')
def tendik_update(request, pk):
    tendik = get_object_or_404(TenagaPendidik, pk=pk, jenis='TENDIK')
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=tendik)
        if form.is_valid():
            form.save()
            catat_audit(request, 'Edit Tendik', f"Memperbarui Tendik: {tendik.nama}")
            messages.success(request, f"Data tendik {tendik.nama} berhasil diperbarui!")
            return redirect('admin_kelola_tendik')
    else:
        form = TenagaPendidikForm(instance=tendik)
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': f'Edit Tendik: {tendik.nama}'})


@login_required(login_url='user_login')
def tendik_delete(request, pk):
    tendik = get_object_or_404(TenagaPendidik, pk=pk, jenis='TENDIK')
    nama = tendik.nama
    tendik.delete()
    catat_audit(request, 'Hapus Tendik', f"Menghapus Tendik: {nama}")
    messages.success(request, f"Data tendik {nama} berhasil dihapus!")
    return redirect('admin_kelola_tendik')


# ==========================================
# 7. ROUTE LAMA TENAGA KEPENDIDIKAN (KOMPATIBILITAS)
# ==========================================

@login_required(login_url='user_login')
def tenaga_kependidikan_create(request):
    return tendik_create(request)


@login_required(login_url='user_login')
def tenaga_kependidikan_update(request, pk):
    return tendik_update(request, pk)


@login_required(login_url='user_login')
def tenaga_kependidikan_delete(request, pk):
    return tendik_delete(request, pk)


# ==========================================
# 8. CRUD MANAJEMEN USER (RBAC VALIDATED)
# ==========================================

@login_required(login_url='user_login')
def user_create(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        messages.error(request, 'Akses ditolak!')
        return redirect('user_login')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            u = form.save()
            catat_audit(request, 'Tambah User', f"Membuat akun user: {u.username} ({u.email})")
            messages.success(request, f"Akun {u.username} berhasil dibuat!")
            return redirect('admin_kelola_user')
    else:
        form = UserForm()
        
    return render(request, 'core/admin/user_form.html', {'form': form, 'title': 'Tambah User Baru'})


@login_required(login_url='user_login')
def user_update(request, pk):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        messages.error(request, 'Akses ditolak!')
        return redirect('user_login')

    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=target_user)
        if form.is_valid():
            u = form.save()
            catat_audit(request, 'Edit User', f"Memperbarui profil user: {u.username}")
            messages.success(request, f"Akun {u.username} berhasil diperbarui!")
            return redirect('admin_kelola_user')
    else:
        form = UserForm(instance=target_user)
    return render(request, 'core/admin/user_form.html', {'form': form, 'title': f'Edit Akun: {target_user.username}'})


@login_required(login_url='user_login')
def user_delete(request, pk):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        messages.error(request, 'Akses ditolak!')
        return redirect('user_login')

    target_user = get_object_or_404(User, pk=pk)
    if target_user == request.user:
        messages.error(request, 'Anda tidak dapat menghapus akun Anda sendiri!')
        return redirect('admin_kelola_user')

    username = target_user.username
    target_user.delete()
    catat_audit(request, 'Hapus User', f"Menghapus user: {username}")
    messages.success(request, f"Akun {username} berhasil dihapus!")
    return redirect('admin_kelola_user')


# ==========================================
# 9. KELOLA SAMBUTAN (CKEDITOR 5)
# ==========================================

@login_required(login_url='user_login')
def admin_kelola_sambutan(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    sambutan = Sambutan.objects.first()
    if not sambutan:
        sambutan = Sambutan.objects.create(
            judul="Sambutan Koordinator Prodi", 
            nama_author="Koordinator Prodi",
            isi="<p>Selamat datang di Program Studi Administrasi Publik.</p>"
        )

    if request.method == 'POST':
        form = SambutanForm(request.POST, request.FILES, instance=sambutan)
        if form.is_valid():
            form.save()
            catat_audit(request, 'Edit Sambutan', 'Memperbarui sambutan koordinator prodi')
            messages.success(request, 'Sambutan Koordinator Prodi berhasil diperbarui!')
            return redirect('admin_kelola_sambutan')
    else:
        form = SambutanForm(instance=sambutan)

    return render(request, 'core/admin/sambutan_form.html', {
        'form': form,
        'title': 'Kelola Sambutan Koordinator Prodi'
    })


# ==========================================
# 10. KELOLA HALAMAN TENTANG (PROFIL, VISI MISI, DLL)
# ==========================================

@login_required(login_url='user_login')
def admin_kelola_tentang(request, kategori='profil'):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    if kategori in ['visi_misi', 'tujuan']:
        return redirect('admin_kelola_visi_misi')

    valid_dict = dict(HalamanTentang.KATEGORI_CHOICES)
    if kategori not in valid_dict:
        return redirect('admin_kelola_tentang', kategori='profil')

    default_judul = valid_dict.get(kategori, 'Halaman Tentang')
    halaman, created = HalamanTentang.objects.get_or_create(
        kategori=kategori,
        defaults={'judul': default_judul, 'isi': '<p>Konten belum diisi.</p>'}
    )

    if request.method == 'POST':
        if request.POST.get('hapus_gambar') == '1' and halaman.gambar:
            halaman.gambar.delete(save=False)
            halaman.gambar = None
            halaman.save()

        form = HalamanTentangForm(request.POST, request.FILES, instance=halaman)
        if form.is_valid():
            form.save()
            catat_audit(request, 'Edit Halaman Tentang', f"Memperbarui konten {halaman.get_kategori_display()}")
            messages.success(request, f"{halaman.get_kategori_display()} berhasil diperbarui!")
            return redirect('admin_kelola_tentang', kategori=kategori)
    else:
        form = HalamanTentangForm(instance=halaman)

    return render(request, 'core/admin/tentang_form.html', {
        'form': form,
        'halaman': halaman,
        'kategori_aktif': kategori,
        'daftar_kategori': HalamanTentang.KATEGORI_CHOICES,
        'title': f"Kelola {halaman.get_kategori_display()}"
    })

def tentang_detail(request, kategori):
    if kategori in ['visi_misi', 'tujuan']:
        visi_obj = VisiMisiTujuan.objects.first()
        context = {
            'halaman': {
                'kategori': kategori,
                'judul': 'Visi, Misi, dan Tujuan',
                'get_kategori_display': 'Visi, Misi, dan Tujuan',
                'updated_at': visi_obj.updated_at if visi_obj else None,
            },
            'kategori': kategori,
            'kategori_aktif': kategori,
            'visi_obj': visi_obj,
            'daftar_misi': visi_obj.misi_items.all() if visi_obj else [],
            'daftar_tujuan': visi_obj.tujuan_items.all() if visi_obj else [],
        }
        return render(request, 'core/admin/tentang_detail.html', context)

    halaman = get_object_or_404(HalamanTentang, kategori=kategori)
    context = {
        'halaman': halaman,
        'kategori': kategori,
    }
    return render(request, 'core/admin/tentang_detail.html', context)

@login_required(login_url='user_login')
def admin_kelola_visi_misi(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    visi_obj, created = VisiMisiTujuan.objects.get_or_create(id=1)

    if request.method == 'POST':
        visi_teks = request.POST.get('visi_teks', '').strip()
        misi_intro = request.POST.get('misi_intro', '').strip()
        tujuan_intro = request.POST.get('tujuan_intro', '').strip()

        if visi_teks:
            visi_obj.visi_teks = visi_teks
        if misi_intro:
            visi_obj.misi_intro = misi_intro
        if tujuan_intro:
            visi_obj.tujuan_intro = tujuan_intro
        visi_obj.save()

        # Update Misi items
        misi_isi_list = request.POST.getlist('misi_isi[]')
        visi_obj.misi_items.all().delete()
        for idx, isi in enumerate(misi_isi_list, start=1):
            isi_clean = isi.strip()
            if isi_clean:
                MisiItem.objects.create(visi_misi=visi_obj, urutan=idx, isi=isi_clean)

        # Update Tujuan items
        tujuan_judul_list = request.POST.getlist('tujuan_judul[]')
        tujuan_subjudul_list = request.POST.getlist('tujuan_subjudul[]')
        tujuan_deskripsi_list = request.POST.getlist('tujuan_deskripsi[]')

        visi_obj.tujuan_items.all().delete()
        for idx in range(len(tujuan_judul_list)):
            judul = tujuan_judul_list[idx].strip()
            subjudul = tujuan_subjudul_list[idx].strip() if idx < len(tujuan_subjudul_list) else ''
            deskripsi = tujuan_deskripsi_list[idx].strip() if idx < len(tujuan_deskripsi_list) else ''
            if judul:
                TujuanItem.objects.create(
                    visi_misi=visi_obj,
                    urutan=idx + 1,
                    judul=judul,
                    subjudul=subjudul,
                    deskripsi=deskripsi
                )

        catat_audit(request, 'Edit Visi Misi Tujuan', 'Memperbarui Visi, Misi, dan Tujuan Program Studi')
        messages.success(request, 'Visi, Misi, dan Tujuan berhasil diperbarui!')
        return redirect('admin_kelola_visi_misi')

    daftar_misi = visi_obj.misi_items.all()
    daftar_tujuan = visi_obj.tujuan_items.all()

    daftar_kategori = [
        ('profil', 'Profil Program Studi'),
        ('visi_misi', 'Visi, Misi & Tujuan'),
        ('sejarah', 'Sejarah Singkat'),
        ('struktur', 'Struktur Organisasi'),
    ]

    context = {
        'visi_obj': visi_obj,
        'daftar_misi': daftar_misi,
        'daftar_tujuan': daftar_tujuan,
        'title': 'Kelola Visi, Misi & Tujuan',
        'kategori_aktif': 'visi_misi',
        'daftar_kategori': daftar_kategori,
    }
    return render(request, 'core/admin/visi_misi_form.html', context)


# ==========================================
# 11. MODUL AKADEMIK PUBLIK & ADMIN
# (SIGA-8, Kurikulum, Jadwal, RPS, Panduan)
# ==========================================

def akademik_detail(request, kategori):
    halaman = get_object_or_404(HalamanAkademik, kategori=kategori)
    daftar_dokumen = halaman.dokumen_list.all()
    context = {
        'halaman': halaman,
        'kategori_aktif': kategori,
        'daftar_kategori': HalamanAkademik.KATEGORI_CHOICES,
        'daftar_dokumen': daftar_dokumen,
    }
    return render(request, 'core/akademik_detail.html', context)


@login_required(login_url='user_login')
def admin_kelola_akademik(request, kategori='siga8'):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    default_judul = dict(HalamanAkademik.KATEGORI_CHOICES).get(kategori, 'Halaman Akademik')
    halaman, created = HalamanAkademik.objects.get_or_create(
        kategori=kategori,
        defaults={'judul': default_judul, 'isi': '<p>Konten akademik belum diisi.</p>'}
    )

    if request.method == 'POST':
        # Cek apakah ini aksi tambah dokumen lampiran baru
        if 'tambah_dokumen' in request.POST:
            judul_doc = request.POST.get('judul_dokumen', '').strip()
            file_doc = request.FILES.get('file_dokumen')
            ket_doc = request.POST.get('keterangan_dokumen', '').strip()
            if judul_doc and file_doc:
                DokumenAkademik.objects.create(
                    halaman=halaman,
                    judul=judul_doc,
                    file=file_doc,
                    keterangan=ket_doc
                )
                catat_audit(request, 'Tambah Dokumen Akademik', f"Menambahkan berkas {judul_doc} ke {halaman.get_kategori_display()}")
                messages.success(request, f"Berkas '{judul_doc}' berhasil diunggah!")
            else:
                messages.error(request, 'Judul dokumen dan file wajib diisi!')
            return redirect('admin_kelola_akademik_kategori', kategori=kategori)

        # Update form utama HalamanAkademik
        form = HalamanAkademikForm(request.POST, request.FILES, instance=halaman)
        if form.is_valid():
            form.save()
            catat_audit(request, 'Edit Halaman Akademik', f"Memperbarui konten {halaman.get_kategori_display()}")
            messages.success(request, f"{halaman.get_kategori_display()} berhasil diperbarui!")
            return redirect('admin_kelola_akademik_kategori', kategori=kategori)
    else:
        form = HalamanAkademikForm(instance=halaman)

    daftar_dokumen = halaman.dokumen_list.all()

    context = {
        'form': form,
        'halaman': halaman,
        'kategori_aktif': kategori,
        'daftar_kategori': HalamanAkademik.KATEGORI_CHOICES,
        'daftar_dokumen': daftar_dokumen,
        'title': f"Kelola {halaman.get_kategori_display()}",
    }
    return render(request, 'core/admin/akademik_form.html', context)


@login_required(login_url='user_login')
def admin_hapus_dokumen_akademik(request, pk):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    dokumen = get_object_or_404(DokumenAkademik, pk=pk)
    kategori = dokumen.halaman.kategori
    nama_doc = dokumen.judul
    dokumen.delete()
    catat_audit(request, 'Hapus Dokumen Akademik', f"Menghapus berkas: {nama_doc}")
    messages.success(request, f"Berkas '{nama_doc}' berhasil dihapus!")
    return redirect('admin_kelola_akademik_kategori', kategori=kategori)

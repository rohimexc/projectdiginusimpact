from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.core.exceptions import ValidationError

from .models import (
    Sambutan, Galeri, Hero, Berita, TenagaPendidik, AuditLog, 
    HalamanTentang, VisiMisiTujuan, MisiItem, TujuanItem, 
    HalamanAkademik, DokumenAkademik, KomentarBerita
)
from .forms import (
    BeritaForm, TenagaPendidikForm, UserForm, SambutanForm, 
    HalamanTentangForm, HalamanAkademikForm, GaleriForm, HeroForm
)
from .validators import validate_image_file, validate_video_file, validate_document_file

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


def _validate_request_files(request, field_validators):
    """Validasi file unggahan pada layer view sesuai jenis dan batas ukurannya."""
    errors = []
    for field_name, validator in field_validators.items():
        uploaded = request.FILES.get(field_name)
        if uploaded:
            try:
                validator(uploaded)
            except ValidationError as exc:
                errors.extend(exc.messages)
    return errors

# ==========================================
# 1. LANDING PAGE & BERITA PUBLIK
# ==========================================

def home(request):
    hero = Hero.objects.filter(is_active=True).first()
    sambutan = Sambutan.objects.first()
    daftar_berita = Berita.objects.all().order_by('-posted_at')[:3]
    daftar_tenaga_kependidikan = TenagaPendidik.objects.filter(jenis='TENDIK')[:4]

    context = {
        'hero': hero,
        'sambutan': sambutan,
        'daftar_berita': daftar_berita,
        'daftar_tenaga_kependidikan': daftar_tenaga_kependidikan,
    }
    return render(request, 'core/index.html', context)


def galeri_list(request):
    # Auto-seed foto kegiatan bila data galeri masih kosong
    if not Galeri.objects.exists():
        sample_galeri = [
            ("Kuliah Umum: Transformasi Digital Sektor Publik", "berita/Untitled_ALVBYOy.png", 1),
            ("Pengabdian Masyarakat di Desa Binaan FISIP", "berita/Untitled_BkdR4hu.png", 2),
            ("Seminar Nasional Kebijakan Publik & Smart Governance", "berita/IMG_0453.JPEG", 3),
            ("Pelatihan Kepemimpinan Mahasiswa Administrasi Publik", "berita/3d80edb0db6f6ab2fa95cf3cf5006344.jpg", 4),
            ("Kunjungan Studi Lapangan Tata Kelola Pemerintahan", "berita/gugugaga.webp", 5),
            ("Rapat Kerja Kurikulum Berbasis OBE & MBKM", "berita/Untitled.png", 6),
        ]
        for judul, gambar, urutan in sample_galeri:
            Galeri.objects.create(judul=judul, gambar=gambar, urutan=urutan)

    query = request.GET.get('q', '').strip()
    galeri_qs = Galeri.objects.all().order_by('urutan', '-created_at')

    if query:
        galeri_qs = galeri_qs.filter(judul__icontains=query)

    paginator = Paginator(galeri_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'total_galeri': galeri_qs.count(),
    }
    return render(request, 'core/galeri/list.html', context)


def berita_list(request):
    # Auto-seed berita bila data berita masih kosong
    if not Berita.objects.exists():
        from django.utils import timezone
        sample_berita = [
            (
                "Kuliah Tamu: Transformasi Digital dan Reformasi Birokrasi Menuju Smart Governance",
                "Program Studi Administrasi Publik menggelar kuliah tamu menghadirkan pakar tata kelola digital untuk membahas reformasi birokrasi era modern.",
                "<p>Program Studi Administrasi Publik FISIP Universitas Tadulako sukses menyelenggarakan Kuliah Tamu bertajuk <strong>'Transformasi Digital dan Reformasi Birokrasi Menuju Smart Governance'</strong>. Acara ini dihadiri oleh ratusan mahasiswa dan dosen, membahas strategi implementasi teknologi dalam peningkatan efisiensi layanan publik di era Society 5.0.</p>",
                "berita/Untitled_ALVBYOy.png",
                128,
                34,
                12,
            ),
            (
                "Pengabdian Masyarakat: Penguatan Kapasitas Administrasi dan Akuntabilitas Desa",
                "Dosen dan mahasiswa Administrasi Publik melaksanakan program pendampingan tata kelola administrasi dan keuangan desa binaan.",
                "<p>Sebagai wujud nyata implementasi Tri Dharma Perguruan Tinggi, tim dosen dan mahasiswa Program Studi Administrasi Publik FISIP Universitas Tadulako melaksanakan kegiatan Pengabdian kepada Masyarakat (PkM) dengan fokus <strong>'Penguatan Kapasitas Aparatur Desa dalam Tata Kelola Administrasi dan Akuntabilitas Publik'</strong>.</p>",
                "berita/Untitled_BkdR4hu.png",
                95,
                27,
                8,
            ),
        ]
        for judul, ringkasan, konten, gambar, views, likes, shares in sample_berita:
            Berita.objects.create(
                judul=judul,
                ringkasan=ringkasan,
                konten=konten,
                gambar=gambar,
                views=views,
                likes=likes,
                shares=shares,
                posted_at=timezone.now(),
            )

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

    # 1. Hitung Views Otomatis (1x per session per berita)
    session_key_view = f'viewed_berita_{pk}'
    if not request.session.get(session_key_view, False):
        Berita.objects.filter(pk=pk).update(views=F('views') + 1)
        request.session[session_key_view] = True
        berita.refresh_from_db()

    # 2. Cek Status Like (warna merah tetap saat refresh)
    session_key_like = f'liked_berita_{pk}'
    is_liked = request.session.get(session_key_like, False)

    # 3. Tangani Pengiriman Komentar
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', '')

        # Jika belum login / belum punya akun -> redirect ke laman login
        if not request.user.is_authenticated:
            messages.info(request, 'Silakan masuk (login) terlebih dahulu untuk mengirim komentar. Jika belum punya akun, Anda dapat mendaftar.')
            login_url = f"{reverse('user_login')}?next={request.path}#komentar-section"
            if is_ajax:
                return JsonResponse({
                    'status': 'redirect',
                    'url': login_url,
                    'message': 'Silakan login terlebih dahulu untuk berkomentar.'
                })
            return redirect(login_url)

        # Jika sudah punya akun & login -> komentar terkirim
        isi = request.POST.get('isi', '').strip()
        if isi:
            nama = request.user.first_name or request.user.username
            email = request.user.email
            komentar = KomentarBerita.objects.create(
                berita=berita,
                user=request.user,
                nama=nama,
                email=email,
                isi=isi
            )
            if is_ajax:
                return JsonResponse({
                    'status': 'success',
                    'message': 'Komentar Anda berhasil dikirim.',
                    'komentar': {
                        'id': komentar.id,
                        'nama': komentar.nama,
                        'username': request.user.username,
                        'inisial': komentar.nama[:2].upper(),
                        'isi': komentar.isi,
                        'tanggal': komentar.created_at.strftime('%d %b %Y, %H:%M'),
                        'can_manage': True
                    },
                    'total_komentar': berita.komentar_list.count()
                })
            messages.success(request, 'Komentar Anda berhasil dikirim.')
            return redirect(f"{reverse('berita_detail', kwargs={'pk': pk})}#komentar-section")
        else:
            if is_ajax:
                return JsonResponse({'status': 'error', 'message': 'Komentar tidak boleh kosong!'}, status=400)
            messages.error(request, 'Komentar tidak boleh kosong!')

    berita_terkait = Berita.objects.exclude(pk=pk).order_by('-posted_at')[:3]
    komentar_list = berita.komentar_list.all().order_by('-created_at')

    context = {
        'berita': berita,
        'berita_terkait': berita_terkait,
        'komentar_list': komentar_list,
        'is_liked': is_liked,
    }
    return render(request, 'core/Berita/detail.html', context)


@require_POST
def berita_like(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    session_key_like = f'liked_berita_{pk}'
    is_liked = request.session.get(session_key_like, False)

    if is_liked:
        if berita.likes > 0:
            Berita.objects.filter(pk=pk).update(likes=F('likes') - 1)
        request.session[session_key_like] = False
        liked = False
    else:
        Berita.objects.filter(pk=pk).update(likes=F('likes') + 1)
        request.session[session_key_like] = True
        liked = True

    berita.refresh_from_db()
    return JsonResponse({
        'status': 'success',
        'liked': liked,
        'likes': berita.likes
    })


@require_POST
def berita_share(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    Berita.objects.filter(pk=pk).update(shares=F('shares') + 1)
    berita.refresh_from_db()
    return JsonResponse({
        'status': 'success',
        'shares': berita.shares
    })


@require_POST
def komentar_edit(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Silakan login terlebih dahulu!'}, status=401)
    komentar = get_object_or_404(KomentarBerita, pk=pk)
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    is_admin = 'admin' in user_role or request.user.is_staff or request.user.is_superuser
    if komentar.user and komentar.user != request.user and not is_admin:
        return JsonResponse({'status': 'error', 'message': 'Anda tidak berhak mengedit komentar ini!'}, status=403)

    isi_baru = request.POST.get('isi', '').strip()
    if not isi_baru:
        return JsonResponse({'status': 'error', 'message': 'Komentar tidak boleh kosong!'}, status=400)

    komentar.isi = isi_baru
    komentar.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Komentar berhasil diperbarui!',
        'isi': komentar.isi
    })


@require_POST
def komentar_hapus(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Silakan login terlebih dahulu!'}, status=401)
    komentar = get_object_or_404(KomentarBerita, pk=pk)
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    is_admin = 'admin' in user_role or request.user.is_staff or request.user.is_superuser
    if komentar.user and komentar.user != request.user and not is_admin:
        return JsonResponse({'status': 'error', 'message': 'Anda tidak berhak menghapus komentar ini!'}, status=403)

    berita = komentar.berita
    komentar.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'Komentar berhasil dihapus!',
        'total_komentar': berita.komentar_list.count()
    })


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
# 2. AUTENTIKASI (EMAIL / USERNAME / REGISTER)
# ==========================================

def user_register(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('home')
    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == 'POST':
        nama_lengkap = request.POST.get('nama_lengkap', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')

        context = {
            'next': next_url,
            'nama_lengkap': nama_lengkap,
            'username': username,
            'email': email
        }

        if not username or not email or not password:
            messages.error(request, 'Semua kolom yang bertanda bintang (*) wajib diisi.')
            return render(request, 'core/register.html', context)

        if password != password_confirm:
            messages.error(request, 'Konfirmasi kata sandi tidak cocok.')
            return render(request, 'core/register.html', context)

        if len(password) < 6:
            messages.error(request, 'Kata sandi minimal 6 karakter.')
            return render(request, 'core/register.html', context)

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, 'Username sudah digunakan. Silakan gunakan username lain.')
            return render(request, 'core/register.html', context)

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, 'Email sudah terdaftar. Silakan gunakan akun Anda untuk masuk.')
            return render(request, 'core/register.html', context)

        # Buat akun baru secara otomatis dengan role USER
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nama_lengkap,
            role=User.Role.USER
        )

        catat_audit(request, 'Registrasi Berhasil', f"User {user.username} ({user.email}) mendaftar dengan role USER.")
        messages.success(request, f"Pendaftaran akun berhasil! Silakan masuk (login) dengan akun Anda terlebih dahulu untuk mulai berkomentar.")

        login_url = reverse('user_login')
        if next_url:
            login_url = f"{login_url}?next={next_url}"
        return redirect(login_url)

    return render(request, 'core/register.html', {'next': next_url})


def user_login(request):
    next_url = request.GET.get('next') or request.POST.get('next') or ''

    if request.user.is_authenticated:
        user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
        if next_url:
            return redirect(next_url)
        if 'admin' in user_role or request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        return redirect('home')

    if request.method == 'POST':
        email_or_user = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not email_or_user or not password:
            messages.error(request, 'Email/Username dan kata sandi wajib diisi.')
            return render(request, 'core/login.html', {'next': next_url})

        user_obj = User.objects.filter(Q(email__iexact=email_or_user) | Q(username__iexact=email_or_user)).first()
        auth_username = user_obj.username if user_obj else email_or_user
        user = authenticate(request, username=auth_username, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request, 'Akun Anda dinonaktifkan. Silakan hubungi admin.')
                return render(request, 'core/login.html', {'next': next_url})

            login(request, user)
            catat_audit(request, 'Login Berhasil', f"User {user.username} ({user.email}) masuk ke sistem.")
            messages.success(request, f"Selamat datang kembali, {user.first_name or user.username}!")

            user_role = getattr(user, 'role', '').lower() if hasattr(user, 'role') and user.role else ''
            if next_url:
                if '/Berita/' in next_url and '#komentar-section' not in next_url:
                    next_url = f"{next_url.rstrip('/')}/#komentar-section"
                return redirect(next_url)
            if 'admin' in user_role or user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Email/Username atau kata sandi yang dimasukkan salah.')

    return render(request, 'core/login.html', {'next': next_url})


def user_logout(request):
    next_url = request.GET.get('next') or ''
    if request.user.is_authenticated:
        catat_audit(request, 'Logout', f"User {request.user.email} keluar.")
    logout(request)
    messages.success(request, 'Anda telah berhasil keluar (logout).')
    if next_url:
        return redirect(next_url)
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
    total_galeri = Galeri.objects.count()
    hero_obj = Hero.objects.filter(is_active=True).first() or Hero.objects.first()
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
        'total_galeri': total_galeri,
        'hero_obj': hero_obj,
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
        upload_errors = _validate_request_files(request, {'gambar': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = BeritaForm(request.POST, request.FILES)
        if not upload_errors and form.is_valid():
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
        upload_errors = _validate_request_files(request, {'gambar': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = BeritaForm(request.POST, request.FILES, instance=berita)
        if not upload_errors and form.is_valid():
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
        upload_errors = _validate_request_files(request, {'foto': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = TenagaPendidikForm(request.POST, request.FILES)
        if not upload_errors and form.is_valid():
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
        upload_errors = _validate_request_files(request, {'foto': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = TenagaPendidikForm(request.POST, request.FILES, instance=dosen)
        if not upload_errors and form.is_valid():
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
        upload_errors = _validate_request_files(request, {'foto': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = TenagaPendidikForm(request.POST, request.FILES)
        if not upload_errors and form.is_valid():
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
        upload_errors = _validate_request_files(request, {'foto': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = TenagaPendidikForm(request.POST, request.FILES, instance=tendik)
        if not upload_errors and form.is_valid():
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
        upload_errors = _validate_request_files(request, {'foto': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = SambutanForm(request.POST, request.FILES, instance=sambutan)
        if not upload_errors and form.is_valid():
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
        upload_errors = _validate_request_files(
            request,
            {'gambar': validate_image_file, 'file_utama': validate_document_file},
        )
        for err in upload_errors:
            messages.error(request, err)

        if not upload_errors and request.POST.get('hapus_gambar') == '1' and halaman.gambar and 'gambar' not in request.FILES:
            halaman.gambar.delete(save=False)
            halaman.gambar = None
            halaman.save()

        form = HalamanTentangForm(request.POST, request.FILES, instance=halaman)
        if not upload_errors and form.is_valid():
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
            judul = source_judul = tujuan_judul_list[idx].strip()
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
        # Cek penambahan dokumen lampiran
        if 'tambah_dokumen' in request.POST:
            judul_doc = request.POST.get('judul_dokumen', '').strip()
            file_doc = request.FILES.get('file_dokumen')
            ket_doc = request.POST.get('keterangan_dokumen', '').strip()
            if judul_doc and file_doc:
                upload_errors = _validate_request_files(request, {'file_dokumen': validate_document_file})
                if upload_errors:
                    for err in upload_errors:
                        messages.error(request, err)
                else:
                    doc = DokumenAkademik(
                        halaman=halaman,
                        judul=judul_doc,
                        file=file_doc,
                        keterangan=ket_doc
                    )
                    doc.full_clean()
                    doc.save()
                    catat_audit(request, 'Tambah Dokumen Akademik', f"Menambahkan berkas {judul_doc} ke {halaman.get_kategori_display()}")
                    messages.success(request, f"Berkas '{judul_doc}' berhasil diunggah!")
            else:
                messages.error(request, 'Judul dokumen dan file wajib diisi!')
            return redirect('admin_kelola_akademik_kategori', kategori=kategori)

        # Update form utama HalamanAkademik
        upload_errors = _validate_request_files(request, {'file_utama': validate_document_file})
        for err in upload_errors:
            messages.error(request, err)
        form = HalamanAkademikForm(request.POST, request.FILES, instance=halaman)
        if not upload_errors and form.is_valid():
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


# ==========================================
# 11. MANAJEMEN GALERI FOTO
# ==========================================

@login_required(login_url='user_login')
def admin_kelola_galeri(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')
    daftar_galeri = Galeri.objects.all().order_by('urutan', '-created_at')
    return render(request, 'core/admin/galeri_kelola.html', {'daftar_galeri': daftar_galeri})


@login_required(login_url='user_login')
def galeri_create(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    if request.method == 'POST':
        upload_errors = _validate_request_files(request, {'gambar': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = GaleriForm(request.POST, request.FILES)
        if not upload_errors and form.is_valid():
            galeri = form.save()
            catat_audit(request, 'Tambah Galeri', f"Menambahkan Foto Galeri: {galeri.judul or 'Foto Galeri'}")
            messages.success(request, 'Foto kegiatan berhasil ditambahkan ke galeri!')
            return redirect('admin_kelola_galeri')
    else:
        last_item = Galeri.objects.order_by('-urutan').first()
        next_urutan = (last_item.urutan + 1) if last_item else 1
        form = GaleriForm(initial={'urutan': next_urutan})

    return render(request, 'core/admin/galeri_form.html', {
        'form': form,
        'title': 'Tambah Foto Galeri Baru'
    })


@login_required(login_url='user_login')
def galeri_update(request, pk):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    galeri = get_object_or_404(Galeri, pk=pk)
    if request.method == 'POST':
        upload_errors = _validate_request_files(request, {'gambar': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = GaleriForm(request.POST, request.FILES, instance=galeri)
        if not upload_errors and form.is_valid():
            form.save()
            catat_audit(request, 'Edit Galeri', f"Memperbarui Foto Galeri #{galeri.id}")
            messages.success(request, 'Data galeri foto berhasil diperbarui!')
            return redirect('admin_kelola_galeri')
    else:
        form = GaleriForm(instance=galeri)

    return render(request, 'core/admin/galeri_form.html', {
        'form': form,
        'galeri': galeri,
        'title': f'Edit Foto Galeri #{galeri.id}'
    })


@login_required(login_url='user_login')
def galeri_delete(request, pk):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    galeri = get_object_or_404(Galeri, pk=pk)
    nama = galeri.judul or f"Foto Galeri #{galeri.id}"
    galeri.delete()
    catat_audit(request, 'Hapus Galeri', f"Menghapus: {nama}")
    messages.success(request, 'Foto galeri berhasil dihapus!')
    return redirect('admin_kelola_galeri')


# ==========================================
# 12. MANAJEMEN HERO BANNER (TUNGGAL)
# ==========================================

@login_required(login_url='user_login')
def admin_kelola_hero(request):
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    hero = Hero.objects.filter(is_active=True).first() or Hero.objects.first()
    if not hero:
        hero = Hero.objects.create(
            subjudul='Program Studi Administrasi Publik',
            judul='Mewujudkan Tata Kelola Publik yang Inovatif & Berintegritas',
            is_active=True,
        )

    if request.method == 'POST':
        upload_errors = _validate_request_files(
            request,
            {'video_file': validate_video_file, 'foto': validate_image_file},
        )
        for err in upload_errors:
            messages.error(request, err)

        form = HeroForm(request.POST, request.FILES, instance=hero)
        if not upload_errors and form.is_valid():
            hero_obj = form.save(commit=False)

            if request.POST.get('hapus_video') == '1' and 'video_file' not in request.FILES:
                if hero_obj.video_file:
                    hero_obj.video_file.delete(save=False)
                hero_obj.video_file = None

            if request.POST.get('hapus_foto') == '1' and 'foto' not in request.FILES:
                if hero_obj.foto:
                    hero_obj.foto.delete(save=False)
                hero_obj.foto = None

            hero_obj.save()
            if hero_obj.is_active:
                Hero.objects.filter(is_active=True).exclude(pk=hero_obj.pk).update(is_active=False)

            catat_audit(request, 'Edit Hero Banner', f"Memperbarui Hero Banner: {hero_obj.judul or 'Hero'}")
            messages.success(request, 'Hero Banner berhasil diperbarui!')
            return redirect('admin_kelola_hero')
    else:
        form = HeroForm(instance=hero)

    return render(request, 'core/admin/hero_form.html', {
        'form': form,
        'hero': hero,
        'title': 'Manajemen Hero Banner',
    })
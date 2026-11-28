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
    HalamanAkademik, DokumenAkademik, KomentarBerita, Event,
    SiteSetting, SocialMedia, QuickLink, SOCIAL_PLATFORM_CHOICES, PLATFORM_ICONS
)
from .forms import (
    BeritaForm, TenagaPendidikForm, UserForm, SambutanForm, 
    HalamanTentangForm, HalamanAkademikForm, GaleriForm, HeroForm, EventForm,
    SiteSettingForm, SocialMediaFormSet, QuickLinkFormSet
)
from .validators import (
    validate_image_file, validate_video_file, validate_document_file,
    validate_favicon_file, validate_site_logo_file
)

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
    daftar_berita = Berita.objects.all().order_by('-posted_at')[:12]
    daftar_galeri = Galeri.objects.all().order_by('urutan', '-created_at')[:12]
    daftar_dosen = TenagaPendidik.objects.filter(jenis='DOSEN').order_by('nama')[:12]
    daftar_tendik = TenagaPendidik.objects.filter(jenis='TENDIK').order_by('nama')[:12]

    # Auto-seed data event jika database masih kosong di server
    if not Event.objects.exists():
        try:
            from datetime import date
            events_data = [
                {
                    'judul': 'Seminar Nasional: Transformasi Digital Tata Kelola Publik Menuju Smart Governance',
                    'slug': 'seminar-nasional-transformasi-digital',
                    'kategori': 'Seminar',
                    'tanggal_mulai': date(2026, 11, 28),
                    'waktu': '08.30 WITA - 12.30 WITA',
                    'lokasi': 'Auditorium FISIP Universitas Tadulako / Zoom Meeting',
                    'poster': 'event_posters/poster_seminar_nasional.jpg',
                    'deskripsi': '<p>Seminar nasional membahas strategi transformasi digital sektor publik dan tata kelola berbasis smart governance.</p>',
                    'link_pendaftaran': 'https://bit.ly/daftar-seminar-ap',
                    'is_active': True,
                },
                {
                    'judul': 'Kuliah Tamu: Kebijakan Publik Berbasis Bukti (Evidence-Based Policy Making)',
                    'slug': 'kuliah-tamu-kebijakan-publik-berbasis-bukti',
                    'kategori': 'Kuliah Tamu',
                    'tanggal_mulai': date(2026, 12, 5),
                    'waktu': '09.00 WITA - 11.30 WITA',
                    'lokasi': 'Ruang Teater FISIP Universitas Tadulako',
                    'poster': 'event_posters/poster_kuliah_tamu.jpg',
                    'deskripsi': '<p>Kuliah tamu bersama pakar kebijakan publik nasional membahas implementasi evidence-based policy making di Indonesia.</p>',
                    'link_pendaftaran': 'https://bit.ly/kuliah-tamu-ap',
                    'is_active': True,
                },
                {
                    'judul': 'Workshop Metodologi Penelitian Kualitatif & Analisis Kebijakan Kontemporer',
                    'slug': 'workshop-metodologi-penelitian-kualitatif',
                    'kategori': 'Workshop',
                    'tanggal_mulai': date(2026, 12, 12),
                    'waktu': '08.00 WITA - 16.00 WITA',
                    'lokasi': 'Lab Komputer & Kebijakan Publik FISIP UNTAD',
                    'poster': 'event_posters/poster_workshop_metopel.jpg',
                    'deskripsi': '<p>Workshop intensif penulisan tugas akhir dan analisis data kualitatif menggunakan NVivo.</p>',
                    'link_pendaftaran': 'https://bit.ly/workshop-metopel-ap',
                    'is_active': True,
                },
                {
                    'judul': 'Rembuk Alumni & Lokakarya Kurikulum Administrasi Publik 2027',
                    'slug': 'rembuk-alumni-lokakarya-kurikulum-2027',
                    'kategori': 'Agenda Prodi',
                    'tanggal_mulai': date(2026, 12, 20),
                    'waktu': '13.00 WITA - Selesai',
                    'lokasi': 'Ruang Rapat Senat FISIP Universitas Tadulako',
                    'poster': 'event_posters/poster_rembuk_alumni.jpg',
                    'deskripsi': '<p>Pertemuan silaturahmi alumni dan peninjauan kurikulum OBE Prodi Administrasi Publik FISIP UNTAD.</p>',
                    'link_pendaftaran': '',
                    'is_active': True,
                },
            ]
            for ev in events_data:
                Event.objects.create(**ev)
        except Exception:
            pass

    daftar_event = Event.objects.filter(is_active=True).order_by('tanggal_mulai', '-created_at')[:10]

    context = {
        'hero': hero,
        'sambutan': sambutan,
        'daftar_berita': daftar_berita,
        'daftar_event': daftar_event,
        'daftar_galeri': daftar_galeri,
        'daftar_dosen': daftar_dosen,
        'daftar_tendik': daftar_tendik,
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

    sorotan_galeri = Galeri.objects.all().order_by('urutan', '-created_at')
    total_galeri = sorotan_galeri.count()

    context = {
        'sorotan_galeri': sorotan_galeri,
        'total_galeri': total_galeri,
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

    import datetime
    from django.utils import timezone

    today = timezone.localdate()

    query = request.GET.get('q', '').strip()
    start_date_str = (request.GET.get('start_date') or request.GET.get('tanggal_mulai', '')).strip()
    end_date_str = (request.GET.get('end_date') or request.GET.get('tanggal_akhir', '')).strip()
    preset = request.GET.get('preset', '').strip()
    sort = request.GET.get('sort', 'terbaru').strip()
    if sort not in ('terbaru', 'terlama'):
        sort = 'terbaru'

    # Tangani Preset Rentang Tanggal Cepat
    if preset == '7d':
        start_date_str = (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        end_date_str = today.strftime('%Y-%m-%d')
    elif preset == 'this_month':
        start_date_str = today.replace(day=1).strftime('%Y-%m-%d')
        end_date_str = today.strftime('%Y-%m-%d')
    elif preset == 'this_year':
        start_date_str = today.replace(month=1, day=1).strftime('%Y-%m-%d')
        end_date_str = today.strftime('%Y-%m-%d')
    elif preset == 'all':
        start_date_str = ''
        end_date_str = ''
        preset = 'all'

    # Deteksi preset aktif bila start_date dan end_date cocok
    if not preset:
        if not start_date_str and not end_date_str:
            preset = 'all'
        elif start_date_str == str(today - datetime.timedelta(days=7)) and end_date_str == str(today):
            preset = '7d'
        elif start_date_str == str(today.replace(day=1)) and end_date_str == str(today):
            preset = 'this_month'
        elif start_date_str == str(today.replace(month=1, day=1)) and end_date_str == str(today):
            preset = 'this_year'

    berita_qs = Berita.objects.all()

    # Filter Kata Kunci
    if query:
        berita_qs = berita_qs.filter(
            Q(judul__icontains=query) | Q(konten__icontains=query) | Q(ringkasan__icontains=query)
        )

    # Filter Rentang Tanggal
    if start_date_str:
        try:
            sd = datetime.date.fromisoformat(start_date_str)
            berita_qs = berita_qs.filter(posted_at__date__gte=sd)
        except ValueError:
            pass

    if end_date_str:
        try:
            ed = datetime.date.fromisoformat(end_date_str)
            berita_qs = berita_qs.filter(posted_at__date__lte=ed)
        except ValueError:
            pass

    # Urutkan
    if sort == 'terlama':
        berita_qs = berita_qs.order_by('posted_at')
    else:
        berita_qs = berita_qs.order_by('-posted_at')

    total_berita = berita_qs.count()

    # Label Filter Aktif untuk Bar Status (Format: DD/MM/YYYY – DD/MM/YYYY)
    active_filter_label = ""
    has_active_filter = bool(query or (start_date_str and preset != 'all') or (end_date_str and preset != 'all'))

    if start_date_str and end_date_str:
        try:
            sd_fmt = datetime.date.fromisoformat(start_date_str).strftime('%d/%m/%Y')
            ed_fmt = datetime.date.fromisoformat(end_date_str).strftime('%d/%m/%Y')
            active_filter_label = f"{sd_fmt} – {ed_fmt}"
        except ValueError:
            active_filter_label = f"{start_date_str} – {end_date_str}"
    elif start_date_str:
        try:
            sd_fmt = datetime.date.fromisoformat(start_date_str).strftime('%d/%m/%Y')
            active_filter_label = f"Mulai {sd_fmt}"
        except ValueError:
            active_filter_label = f"Mulai {start_date_str}"
    elif end_date_str:
        try:
            ed_fmt = datetime.date.fromisoformat(end_date_str).strftime('%d/%m/%Y')
            active_filter_label = f"Sampai {ed_fmt}"
        except ValueError:
            active_filter_label = f"Sampai {end_date_str}"
    elif query:
        active_filter_label = f'"{query}"'

    paginator = Paginator(berita_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'preset': preset,
        'sort': sort,
        'total_berita': total_berita,
        'has_active_filter': has_active_filter,
        'active_filter_label': active_filter_label,
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

    berita_terkait = Berita.objects.exclude(pk=pk).order_by('-posted_at')[:9]
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
    query = request.GET.get('q', '').strip()
    selected_jabatan = request.GET.get('jabatan', '').strip()

    dosen_qs = TenagaPendidik.objects.filter(jenis='DOSEN')

    # Hitung jumlah per jabatan fungsional secara dinamis dari database
    total_dosen = dosen_qs.count()
    count_guru_besar = dosen_qs.filter(Q(jabatan_fungsional__iexact='Guru Besar') | Q(status__iexact='PROFESOR')).count()
    count_lektor_kepala = dosen_qs.filter(jabatan_fungsional__iexact='Lektor Kepala').count()
    count_lektor = dosen_qs.filter(jabatan_fungsional__iexact='Lektor').count()
    count_asisten_ahli = dosen_qs.filter(jabatan_fungsional__iexact='Asisten Ahli').count()

    jabatan_counts = {
        'all': total_dosen,
        'guru_besar': count_guru_besar,
        'lektor_kepala': count_lektor_kepala,
        'lektor': count_lektor,
        'asisten_ahli': count_asisten_ahli,
    }

    # Filter Jabatan Fungsional
    if selected_jabatan:
        if selected_jabatan.lower() == 'guru besar':
            dosen_qs = dosen_qs.filter(Q(jabatan_fungsional__iexact='Guru Besar') | Q(status__iexact='PROFESOR'))
        else:
            dosen_qs = dosen_qs.filter(jabatan_fungsional__iexact=selected_jabatan)

    # Filter Kata Kunci (Nama, NIP, NIDN, Bidang Keahlian/Ilmu)
    if query:
        dosen_qs = dosen_qs.filter(
            Q(nama__icontains=query) |
            Q(nip__icontains=query) |
            Q(nidn__icontains=query) |
            Q(bidang_ilmu__icontains=query)
        )

    dosen_qs = dosen_qs.order_by('nama')

    has_active_filter = bool(query or selected_jabatan)

    context = {
        'daftar_dosen': dosen_qs,
        'dosen_list': dosen_qs,
        'query': query,
        'selected_jabatan': selected_jabatan,
        'jabatan_counts': jabatan_counts,
        'has_active_filter': has_active_filter,
    }
    return render(request, 'core/dosen/list.html', context)


def tenaga_pendidik_detail(request, pk):
    dosen = get_object_or_404(TenagaPendidik, pk=pk, jenis='DOSEN')
    dosen_lainnya = TenagaPendidik.objects.filter(jenis='DOSEN').exclude(pk=pk).order_by('nama')[:12]
    return render(request, 'core/dosen/detail.html', {'dosen': dosen, 'dosen_lainnya': dosen_lainnya})


def tenaga_kependidikan_list(request):
    query = request.GET.get('q', '').strip()
    kependidikan_qs = TenagaPendidik.objects.filter(jenis='TENDIK').order_by('nama')

    if query:
        kependidikan_qs = kependidikan_qs.filter(
            Q(nama__icontains=query) |
            Q(nidn__icontains=query) |
            Q(bidang_ilmu__icontains=query) |
            Q(status__icontains=query)
        )

    context = {
        'tenaga_kependidikan_list': kependidikan_qs,
        'query': query,
    }
    return render(request, 'core/kependidikan/list.html', context)


def tenaga_kependidikan_detail(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    tendik_lainnya = TenagaPendidik.objects.filter(jenis='TENDIK').exclude(pk=pk).order_by('nama')[:12]
    return render(request, 'core/kependidikan/detail.html', {
        'tenaga_kependidikan': tenaga_kependidikan,
        'tendik_lainnya': tendik_lainnya
    })


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

    total_event = Event.objects.count()
    event_aktif = Event.objects.filter(is_active=True).count()
    daftar_event_terdekat = Event.objects.all().order_by('tanggal_mulai', '-created_at')[:4]

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
        'total_event': total_event,
        'event_aktif': event_aktif,
        'daftar_event_terdekat': daftar_event_terdekat,
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
    # Requirement 2: Direct link SIGA-8 -> langsung redirect ke URL eksternal resmi
    if kategori in ('siga8', 'siga'):
        return redirect('https://siga-8.untad.ac.id')

    default_judul = dict(HalamanAkademik.KATEGORI_CHOICES).get(kategori, 'Layanan Akademik')
    halaman, created = HalamanAkademik.objects.get_or_create(
        kategori=kategori,
        defaults={'judul': default_judul, 'isi': ''}
    )

    kondisi = halaman.get_kondisi_tampilan()

    # Requirement 3: Kondisi A (Hanya Link yang diisi) -> langsung redirect ke link tersebut
    if kondisi == 'A' and halaman.link_eksternal:
        return redirect(halaman.link_eksternal)

    daftar_dokumen = halaman.dokumen_list.all()
    context = {
        'halaman': halaman,
        'kategori_aktif': kategori,
        'daftar_kategori': HalamanAkademik.KATEGORI_CHOICES,
        'daftar_dokumen': daftar_dokumen,
        'kondisi': kondisi,
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


# ==========================================
# 13. EVENT & AGENDA TERDEKAT (PUBLIK & ADMIN CRUD)
# ==========================================

def event_list(request):
    """Halaman publik katalog seluruh event / agenda program studi"""
    events = Event.objects.filter(is_active=True)
    
    # 1. Filter Pencarian Keyword
    q = request.GET.get('q', '').strip()
    if q:
        events = events.filter(
            Q(judul__icontains=q) | 
            Q(lokasi__icontains=q) | 
            Q(deskripsi__icontains=q)
        )
    
    # 2. Filter Kategori
    kategori_selected = request.GET.get('kategori', '').strip()
    if kategori_selected:
        events = events.filter(kategori=kategori_selected)

    # 3. Urutkan berdasarkan tanggal terdekat
    events = events.order_by('tanggal_mulai', '-created_at')

    # 4. Pagination (8 kartu per halaman)
    paginator = Paginator(events, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    kategori_list = [k[0] for k in Event.KATEGORI_CHOICES]

    context = {
        'page_obj': page_obj,
        'events': page_obj.object_list,
        'total_event': paginator.count,
        'q': q,
        'kategori_selected': kategori_selected,
        'kategori_list': kategori_list,
    }
    return render(request, 'core/event/list.html', context)


def event_detail(request, slug):
    """Halaman publik detail lengkap satu event / agenda"""
    event = None
    if slug.isdigit():
        event = Event.objects.filter(Q(slug=slug) | Q(pk=int(slug))).first()
    else:
        event = Event.objects.filter(slug=slug).first()
    
    if not event:
        event = get_object_or_404(Event, slug=slug)

    event_lainnya = Event.objects.filter(is_active=True).exclude(pk=event.pk).order_by('tanggal_mulai', '-created_at')[:9]

    context = {
        'event': event,
        'event_lainnya': event_lainnya,
    }
    return render(request, 'core/event/detail.html', context)


@login_required(login_url='user_login')
def admin_kelola_event(request):
    """Halaman tabel manajemen CRUD Event di Admin Portal"""
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')
    daftar_event = Event.objects.all().order_by('tanggal_mulai', '-created_at')
    return render(request, 'core/admin/event_kelola.html', {'daftar_event': daftar_event})


@login_required(login_url='user_login')
def event_create(request):
    """Tambah data event / agenda baru"""
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    if request.method == 'POST':
        upload_errors = _validate_request_files(request, {'poster': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = EventForm(request.POST, request.FILES)
        if not upload_errors and form.is_valid():
            event = form.save()
            catat_audit(request, 'Tambah Event', f"Menambahkan Event: {event.judul}")
            messages.success(request, f'Event "{event.judul}" berhasil ditambahkan!')
            return redirect('admin_kelola_event')
    else:
        form = EventForm()

    return render(request, 'core/admin/event_form.html', {
        'form': form,
        'title': 'Tambah Event / Agenda Baru',
    })


@login_required(login_url='user_login')
def event_update(request, pk):
    """Ubah / perbarui data event"""
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        upload_errors = _validate_request_files(request, {'poster': validate_image_file})
        for err in upload_errors:
            messages.error(request, err)
        form = EventForm(request.POST, request.FILES, instance=event)
        if not upload_errors and form.is_valid():
            form.save()
            catat_audit(request, 'Edit Event', f"Memperbarui Event #{event.id} ({event.judul})")
            messages.success(request, f'Data event "{event.judul}" berhasil diperbarui!')
            return redirect('admin_kelola_event')
    else:
        form = EventForm(instance=event)

    return render(request, 'core/admin/event_form.html', {
        'form': form,
        'event': event,
        'title': f'Edit Event: {event.judul}',
    })


@login_required(login_url='user_login')
def event_delete(request, pk):
    """Hapus data event"""
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    event = get_object_or_404(Event, pk=pk)
    judul = event.judul
    event.delete()
    catat_audit(request, 'Hapus Event', f"Menghapus Event: {judul}")
    messages.success(request, f'Event "{judul}" berhasil dihapus.')
    return redirect('admin_kelola_event')


@login_required(login_url='user_login')
def event_toggle_status(request, pk):
    """Toggle status aktif / nonaktif tampilan event di beranda"""
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    event = get_object_or_404(Event, pk=pk)
    event.is_active = not event.is_active
    event.save(update_fields=['is_active'])
    status_str = "diaktifkan" if event.is_active else "dinonaktifkan"
    catat_audit(request, 'Toggle Status Event', f"Event #{event.id} {status_str}")
    messages.success(request, f'Status event "{event.judul}" berhasil {status_str}!')
    return redirect('admin_kelola_event')


# =========================================================================
# MANAJEMEN PENGATURAN SITUS (SITE SETTINGS) - KHUSUS ROLE ADMIN
# =========================================================================

@login_required(login_url='user_login')
def admin_kelola_pengaturan(request):
    """
    Halaman manajemen Site Settings terpadu:
    - Identitas Situs & Header (Favicon, Logo, Judul, Subjudul)
    - Pengaturan Footer (Logo Footer, Judul, Subjudul, Deskripsi, Alamat Singkat)
    - Kontak & Sosial Media (Alamat, Telepon, WhatsApp, Email, & Relasi Akun Sosmed)
    - Tautan Cepat (Daftar Layanan & Portal Kampus beserta berkas dokumen)
    """
    user_role = getattr(request.user, 'role', '').lower() if hasattr(request.user, 'role') and request.user.role else ''
    if not ('admin' in user_role or request.user.is_staff or request.user.is_superuser):
        logout(request)
        return redirect('user_login')

    setting = SiteSetting.get_settings()

    if request.method == 'POST':
        form = SiteSettingForm(request.POST, request.FILES, instance=setting)
        social_formset = SocialMediaFormSet(request.POST, instance=setting, prefix='social')
        quick_formset = QuickLinkFormSet(request.POST, request.FILES, instance=setting, prefix='quick')

        # Penanganan Hapus Gambar Eksplisit jika dicentang
        if request.POST.get('hapus_favicon') == '1' and 'favicon' not in request.FILES:
            if setting.favicon:
                setting.favicon.delete(save=False)
            setting.favicon = None

        if request.POST.get('hapus_header_logo') == '1' and 'header_logo' not in request.FILES:
            if setting.header_logo:
                setting.header_logo.delete(save=False)
            setting.header_logo = None

        if request.POST.get('hapus_footer_logo') == '1' and 'footer_logo' not in request.FILES:
            if setting.footer_logo:
                setting.footer_logo.delete(save=False)
            setting.footer_logo = None

        if form.is_valid() and social_formset.is_valid() and quick_formset.is_valid():
            form.save()
            social_formset.save()
            quick_formset.save()
            catat_audit(request, 'Update Site Settings', 'Memperbarui konfigurasi identitas situs, footer, kontak, dan tautan')
            messages.success(request, 'Pengaturan website, sosial media, dan tautan cepat berhasil diperbarui!')
            active_tab = request.POST.get('active_tab', 'identitas')
            return redirect(f"{reverse('admin_kelola_pengaturan')}?tab={active_tab}")
        else:
            messages.error(request, 'Terdapat kesalahan pada formulir pengaturan. Silakan periksa tab terkait.')
    else:
        form = SiteSettingForm(instance=setting)
        social_formset = SocialMediaFormSet(instance=setting, prefix='social')
        quick_formset = QuickLinkFormSet(instance=setting, prefix='quick')

    active_tab = request.GET.get('tab', 'identitas')

    context = {
        'setting': setting,
        'form': form,
        'social_formset': social_formset,
        'quick_formset': quick_formset,
        'active_tab': active_tab,
        'social_choices': SOCIAL_PLATFORM_CHOICES,
        'platform_icons': PLATFORM_ICONS,
    }
    return render(request, 'core/admin/pengaturan_form.html', context)


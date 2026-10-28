from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.models import User
from .models import (
    Sambutan, Galeri, Berita, Akademik, TenagaPendidik, Akreditasi, Kontak, AuditLog, Dosen,
    TentangPage, VisiMisiTujuan, MisiItem, TujuanItem,
    AkademikPage, DokumenAkademik
)
from django.db.models import Q
from .forms import (
    BeritaForm, LoginForm, TenagaPendidikForm, AdminUserCreateForm, AdminUserUpdateForm, 
    CustomAuthenticationForm, DosenForm, TentangPageForm,
    VisiMisiTujuanForm, MisiItemForm, TujuanItemForm,
    AkademikPageForm, DokumenAkademikForm
)
from django.core.paginator import Paginator
from akun.views import catat_riwayat_login
from akun.models import RiwayatLogin, UserProfile
from django.utils import timezone

def index(request):
    berita_list = Berita.objects.all().order_by('-post_date')[:3] # Ambil 3 berita terbaru
    galeri_list = Galeri.objects.all()
    akademik_list = Akademik.objects.all()
    staf_list = TenagaPendidik.objects.all()
    akreditasi = Akreditasi.objects.first()
    kontak = Kontak.objects.first()
    sambutan = Sambutan.objects.first()

    context = {
        'berita_list': berita_list,
        'galeri_list': galeri_list,
        'akademik_list': akademik_list,
        'staf_list': staf_list,
        'akreditasi': akreditasi,
        'kontak': kontak,
        'sambutan': sambutan,
    }
    return render(request, 'landing/index.html', context)

def tentang(request):
    sambutan = Sambutan.objects.last()
    return render(request, 'landing/tentang.html', {'sambutan': sambutan})

def akademik(request):
    first_page = AkademikPage.objects.filter(is_active=True).first()
    if first_page:
        return redirect('landing:detail_akademik', slug=first_page.slug)
    return redirect('landing:landing_home')

# 1. Halaman Daftar Berita (DENGAN SEARCH & FILTER TANGGAL)
def berita_list_view(request):
    berita_list = Berita.objects.all().order_by('-post_date')

    # Fitur Search berdasarkan judul atau konten
    query = request.GET.get('q')
    if query:
        berita_list = berita_list.filter(judul__icontains=query) | berita_list.filter(konten__icontains=query)

    # Fitur Filter berdasarkan Tanggal, Bulan, Tahun
    tanggal = request.GET.get('tanggal')
    bulan = request.GET.get('bulan')
    tahun = request.GET.get('tahun')

    if tanggal:
        berita_list = berita_list.filter(post_date__day=tanggal)
    if bulan:
        berita_list = berita_list.filter(post_date__month=bulan)
    if tahun:
        berita_list = berita_list.filter(post_date__year=tahun)

    context = {
        'berita_list': berita_list,
    }
    return render(request, 'landing/berita/berita_list.html', context)

# 2. Halaman Detail (Single Berita saat "Baca Selengkapnya" diklik)
def berita_detail_view(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    return render(request, 'landing/berita/berita_detail.html', {'berita': berita})

@login_required(login_url='landing:login')
def berita_create_view(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES)
        if form.is_valid():
            berita = form.save(commit=False)
            berita.post_date = timezone.now()  # <--- Isi tanggal otomatis di sini
            berita.save()
            
            # Catat ke audit log
            catat_log(request, request.user, f"Menambahkan berita baru berjudul: '{berita.judul}'", "Berita berhasil dipublikasikan")
            
            messages.success(request, "Berita berhasil dipublikasikan!")
            return redirect('landing:dashboard_berita')
    else:
        form = BeritaForm()
    
    return render(request, 'landing/berita/berita_form.html', {'form': form})

# 4. Update Berita (Edit)
@login_required(login_url='landing:login')
def berita_update_view(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES, instance=berita)
        if form.is_valid():
            form.save()
            catat_log(request, request.user, f"Mengubah berita berjudul: '{berita.judul}'", "Berita berhasil diperbarui")
            messages.success(request, "Berita berhasil diperbarui!")
            return redirect('landing:dashboard_berita') # Mengarah ke dashboard admin berita
    else:
        form = BeritaForm(instance=berita)
    return render(request, 'landing/berita/berita_form.html', {'form': form, 'berita': berita})

# 5. Delete Berita (Hapus)
@login_required(login_url='landing:login')
def dashboard_berita_view(request):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "Akses ditolak!")
        return redirect('landing:login')
        
    berita_list = Berita.objects.all().order_by('-post_date')
    
    # Ambil slug dari parameter URL ?hapus=...
    slug_hapus = request.GET.get('hapus')
    delete_berita = None
    if slug_hapus:
        delete_berita = get_object_or_404(Berita, slug=slug_hapus)

    return render(request, 'landing/admin/dashboard_berita.html', {
        'berita_list': berita_list,
        'delete_berita': delete_berita
    })

@login_required(login_url='landing:login')
def berita_delete_view(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    if request.method == 'POST':
        judul_berita = berita.judul
        berita.delete()
        messages.success(request, "Data berita berhasil dihapus!")
        catat_log(request, request.user, f"Menghapus berita: '{judul_berita}'", "Berita dihapus dari sistem")
        return redirect('landing:dashboard_berita')  # <-- Ganti 'berita_list' jadi ini
    
    return render(request, 'landing/admin/dashboard_berita.html', {'berita': berita, 'delete_mode': True})

# Halaman Publik Tendik & Dosen (Bisa diakses siapa saja tanpa login admin)
def tenaga_pendidik_beranda_view(request):
    pendidik_list = TenagaPendidik.objects.all().order_by('nama')
    return render(request, 'landing/TenagaPendidik/Tenaga_Pendidik.html', {
        'pendidik_list': pendidik_list,
        'staf_list': pendidik_list,
        'tendik_list': pendidik_list
    })

# 1. READ / HALAMAN KELOLA TENDIK & DOSEN (Dilengkapi Modal Hapus)
@login_required(login_url='landing:login')
def tenaga_pendidik_view(request):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "Akses ditolak!")
        return redirect('landing:login')
        
    tendik_list = TenagaPendidik.objects.all().order_by('nama')
    
    # Ambil ID dari parameter URL ?hapus=...
    id_hapus = request.GET.get('hapus')
    delete_tendik = None
    if id_hapus:
        delete_tendik = get_object_or_404(TenagaPendidik, pk=id_hapus)

    return render(request, 'landing/admin/dashboard_tendik.html', {
        'tendik_list': tendik_list,
        'delete_tendik': delete_tendik
    })

# 2. CREATE / TAMBAH TENDIK
@login_required(login_url='landing:login')
def tendik_create_view(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            tendik_baru = form.save()
            catat_log(request, request.user, f"Menambahkan data tendik baru: '{tendik_baru.nama}'", "Data tendik ditambahkan")
            messages.success(request, "Data tenaga pendidik berhasil ditambahkan!")
            return redirect('landing:tenaga_pendidik')
    else:
        form = TenagaPendidikForm()
    return render(request, 'landing/TenagaPendidik/tendik_form.html', {'form': form})


# 3. UPDATE / EDIT TENDIK
@login_required(login_url='landing:login')
def tendik_update_view(request, pk):
    tendik = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=tendik)
        if form.is_valid():
            form.save()
            catat_log(request, request.user, f"Memperbarui data tendik: '{tendik.nama}'", "Data tendik diperbarui")
            messages.success(request, "Data tenaga pendidik berhasil diperbarui!")
            return redirect('landing:tenaga_pendidik')
    else:
        form = TenagaPendidikForm(instance=tendik)
    return render(request, 'landing/TenagaPendidik/tendik_form.html', {'form': form, 'tendik': tendik})


# 4. DELETE / HAPUS TENDIK
@login_required(login_url='landing:login')
def tendik_delete_view(request, pk):
    tendik = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        nama_tendik = tendik.nama 
        tendik.delete()
        catat_log(request, request.user, f"Menghapus data tendik: '{nama_tendik}'", "Data tendik dihapus")
        messages.success(request, "Data tenaga pendidik berhasil dihapus!")
        return redirect('landing:tenaga_pendidik')
    return redirect('landing:tenaga_pendidik')

def galeri_page(request):
    galeri_list = Galeri.objects.all()
    return render(request, 'landing/galeri.html', {'galeri_list': galeri_list})

def akreditasi_page(request):
    akreditasi = Akreditasi.objects.last()
    return render(request, 'landing/akreditasi.html', {'akreditasi': akreditasi})

def login_view(request):
    if request.method == 'POST':
        email_input = request.POST.get('username') 
        password_input = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email=email_input)
            username_asli = user_obj.username
        except User.DoesNotExist:
            username_asli = email_input 
            
        user = authenticate(request, username=username_asli, password=password_input)
            
        if user is not None:
            login(request, user)
            catat_riwayat_login(user, request)
            messages.success(request, f"Selamat datang, {user.get_full_name() or user.username}!")
            
            if user.is_superuser or user.is_staff:
                return redirect('landing:dashboard_admin') 
            else:
                messages.error(request, "Akun Anda bukan Admin! Tidak memiliki hak akses.")
                logout(request)
                return redirect('landing:login')
        else:
            messages.error(request, "Email atau password salah.")
            
    form = CustomAuthenticationForm()
    return render(request, 'landing/Login/login.html', {'form': form})

@login_required(login_url='landing:login')
def dashboard_admin_khusus(request):
    # Total Dosen: Hanya jika kategori atau status persis mengandung kata 'DOSEN'
    total_dosen = TenagaPendidik.objects.filter(
        Q(status__icontains='DOSEN') | Q(kategori__icontains='DOSEN')
    ).count()
    
    # Total Tendik: Semua data yang TIDAK mengandung kata 'DOSEN' di status maupun kategorinya
    total_tendik = TenagaPendidik.objects.exclude(
        Q(status__icontains='DOSEN') | Q(kategori__icontains='DOSEN')
    ).count()
    
    total_berita = Berita.objects.count()
    
    jml_dosen_l = TenagaPendidik.objects.filter(
        Q(status__icontains='DOSEN') | Q(kategori__icontains='DOSEN'), jk='L'
    ).count()
    jml_dosen_p = TenagaPendidik.objects.filter(
        Q(status__icontains='DOSEN') | Q(kategori__icontains='DOSEN'), jk='P'
    ).count()
    
    jml_tendik_l = TenagaPendidik.objects.filter(jk='L').exclude(
        Q(status__icontains='DOSEN') | Q(kategori__icontains='DOSEN')
    ).count()
    jml_tendik_p = TenagaPendidik.objects.filter(jk='P').exclude(
        Q(status__icontains='DOSEN') | Q(kategori__icontains='DOSEN')
    ).count()
    
    jml_berita_aktif = Berita.objects.filter(status='A').count() if hasattr(Berita, 'status') else total_berita
    jml_berita_draft = Berita.objects.filter(status='D').count() if hasattr(Berita, 'status') else 0
    
    log_aktivitas = AuditLog.objects.all().order_by('-waktu')

    context = {
        'total_dosen': total_dosen,
        'jml_dosen_l': jml_dosen_l,
        'jml_dosen_p': jml_dosen_p,
        'total_tendik': total_tendik,
        'jml_tendik_l': jml_tendik_l,
        'jml_tendik_p': jml_tendik_p,
        'total_berita': total_berita,
        'jml_berita_aktif': jml_berita_aktif,
        'jml_berita_draft': jml_berita_draft,
        'log_aktivitas': log_aktivitas,
    }
    return render(request, 'landing/admin/dashboard.html', context)

# --- FUNGSI HELPER UNTUK MENGAMBIL IP & CATAT LOG SECARA AMAN ---
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def catat_log(request_or_user, user_or_aktivitas, aktivitas_or_keterangan="", keterangan_opsional=""):
    if hasattr(request_or_user, 'META'): 
        request = request_or_user
        user = user_or_aktivitas
        aktivitas = aktivitas_or_keterangan
        keterangan = keterangan_opsional
    else: 
        request = None
        user = request_or_user
        aktivitas = user_or_aktivitas
        keterangan = aktivitas_or_keterangan

    ip = get_client_ip(request) if request else "-"
    
    # Pastikan jika keterangan kosong, diisi teks yang jelas atau argumennya masuk
    final_keterangan = keterangan if keterangan else "Aktivitas berhasil dilakukan"
    
    AuditLog.objects.create(
        user=user,
        aktivitas=aktivitas,
        keterangan=final_keterangan,
        ip_address=ip
    )


@login_required(login_url='landing:login')
def manajemen_user_view(request):
    users = User.objects.all().order_by('-date_joined')
    riwayat_login = RiwayatLogin.objects.all().order_by('-waktu_login')
    
    context = {
        'users': users,
        'riwayat_login': riwayat_login,
    }
    return render(request, 'landing/User/manajemen_user.html', context)

@login_required(login_url='landing:login')
def user_create_view(request):
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            catat_log(request, request.user, f"Menambahkan akun administrator baru: '{new_user.username}'", "Akun baru berhasil dibuat")
            messages.success(request, "Akun administrator baru berhasil ditambahkan!")
            return redirect('landing:manajemen_user')
    else:
        form = AdminUserCreateForm()
    
    return render(request, 'landing/User/user_form.html', {'form': form})

@login_required(login_url='landing:login')
def user_update_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak!")
        return redirect('landing:manajemen_user')
        
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            catat_log(request, request.user, f"Memperbarui akun administrator: '{target_user.username}'", "Berhasil memperbarui data user")
            messages.success(request, "Akun administrator berhasil diperbarui!")
            return redirect('landing:manajemen_user')
    else:
        form = AdminUserUpdateForm(instance=target_user)
        
    return render(request, 'landing/User/user_form.html', {'form': form, 'target_user': target_user})

@login_required(login_url='landing:login')
def user_delete_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        target_user.is_active = False
        target_user.save()
        
        catat_log(request, request.user, f"Melakukan soft delete / menonaktifkan akun: '{target_user.username}'", "Akun dinonaktifkan")
        messages.success(request, "Akun berhasil dinonaktifkan (Soft Delete).")
        return redirect('landing:manajemen_user')
        
    return render(request, 'landing/User/user_confirm_delete.html', {'target_user': target_user})



@login_required(login_url='landing:login')
def dashboard_dosen(request):
    # Mengambil seluruh data dari model Dosen yang baru
    dosen_list = Dosen.objects.all().order_by('-id')
    
    # Logika modal konfirmasi hapus via query parameter ?hapus=ID
    delete_dosen = None
    dosen_id = request.GET.get('hapus')
    if dosen_id:
        delete_dosen = get_object_or_404(Dosen, id=dosen_id)

    context = {
        'dosen_list': dosen_list,
        'delete_dosen': delete_dosen,
    }
    return render(request, 'landing/admin/dashboard_dosen.html', context)

@login_required(login_url='landing:login')
def dosen_create(request):
    if request.method == 'POST':
        form = DosenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Data dosen berhasil ditambahkan!")
            return redirect('landing:dashboard_dosen')
    else:
        form = DosenForm()
    
    return render(request, 'landing/Dosen/dosen_form.html', {'form': form, 'action': 'Tambah'})

@login_required(login_url='landing:login')
def dosen_update(request, pk):
    dosen = get_object_or_404(Dosen, pk=pk)
    if request.method == 'POST':
        form = DosenForm(request.POST, request.FILES, instance=dosen)
        if form.is_valid():
            form.save()
            messages.success(request, "Data dosen berhasil diperbarui!")
            return redirect('landing:dashboard_dosen')
    else:
        form = DosenForm(instance=dosen)
        
    return render(request, 'landing/Dosen/dosen_form.html', {'form': form, 'action': 'Ubah'})

@login_required(login_url='landing:login')
def dosen_delete(request, pk):
    dosen = get_object_or_404(Dosen, pk=pk)
    if request.method == 'POST':
        nama_dosen = dosen.nama
        dosen.delete()
        messages.success(request, f"Data dosen '{nama_dosen}' berhasil dihapus!")
        return redirect('landing:dashboard_dosen')
    return redirect('landing:dashboard_dosen')

@login_required(login_url='landing:login')
def dosen_delete(request, pk):
    dosen = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        nama_dosen = dosen.nama
        dosen.delete()
        messages.success(request, f"Data dosen '{nama_dosen}' berhasil dihapus!")
        return redirect('landing:dashboard_dosen')
    return redirect('landing:dashboard_dosen')

@login_required(login_url='landing:login')
def dashboard_tentang(request):
    tentang_list = TentangPage.objects.exclude(slug__in=['visi', 'tujuan', 'visimisi', 'visi-misi']).order_by('id')
    
    # Ambil sub-menu yang sedang dipilih untuk diedit (dari param ?edit=<id> atau item pertama)
    edit_id = request.GET.get('edit')
    selected_item = None
    if edit_id:
        selected_item = TentangPage.objects.filter(pk=edit_id).exclude(slug__in=['visi', 'tujuan', 'visimisi', 'visi-misi']).first()
    if not selected_item and tentang_list.exists():
        selected_item = tentang_list.first()

    # Jika ada POST untuk update konten sub-menu
    if request.method == 'POST' and 'update_tentang' in request.POST:
        target_id = request.POST.get('target_id')
        target_item = get_object_or_404(TentangPage, pk=target_id)
        edit_form = TentangPageForm(request.POST, instance=target_item)
        if edit_form.is_valid():
            edit_form.save()
            catat_log(request, request.user, f"Memperbarui Konten Sub-Menu: '{target_item.judul}'", "Konten berhasil disimpan")
            messages.success(request, f"Konten sub-menu '{target_item.judul}' berhasil diperbarui!")
            return redirect(f"/admin-portal/tentang/?edit={target_item.pk}#editPanel")
        else:
            messages.error(request, "Terjadi kesalahan saat menyimpan formulir. Silakan periksa kembali.")
            selected_item = target_item
    else:
        edit_form = TentangPageForm(instance=selected_item) if selected_item else None

    context = {
        'tentang_list': tentang_list,
        'selected_item': selected_item,
        'edit_form': edit_form,
    }
    return render(request, 'landing/admin/dashboard_tentang.html', context)


@login_required(login_url='landing:login')
def dashboard_tentang_edit(request, pk):
    item = get_object_or_404(TentangPage, pk=pk)
    if item.slug in ['visi', 'tujuan', 'visimisi', 'visi-misi']:
        return redirect('landing:dashboard_visi_misi_tujuan')
    return redirect(f"/admin-portal/tentang/?edit={pk}#editPanel")


# --- MANAJEMEN VISI, MISI, DAN TUJUAN ---
@login_required(login_url='landing:login')
def dashboard_visi_misi_tujuan(request):
    visi_misi_obj, _ = VisiMisiTujuan.objects.get_or_create(
        id=1,
        defaults={
            'visi': 'Menjadi Program Studi Administrasi Publik yang unggul secara global dan bereputasi nasional dalam pengembangan ilmu administrasi publik dan tata kelola pemerintahan yang adaptif, berintegritas, dan berwawasan lingkungan.',
            'pengantar_misi': 'Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki misi sebagai berikut:',
            'pengantar_tujuan': 'Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki tujuan Pendidikan berupa:'
        }
    )

    if request.method == 'POST':
        form_visi = VisiMisiTujuanForm(request.POST, instance=visi_misi_obj)
        if form_visi.is_valid():
            form_visi.save()
            catat_log(request, request.user, "Memperbarui Rumusan Visi & Kalimat Pengantar", "Data Visi & Pengantar berhasil diperbarui")
            messages.success(request, "Visi dan kalimat pengantar berhasil diperbarui!")
            return redirect('landing:dashboard_visi_misi_tujuan')
        else:
            messages.error(request, "Terjadi kesalahan saat menyimpan Visi. Periksa kembali form.")
    else:
        form_visi = VisiMisiTujuanForm(instance=visi_misi_obj)

    misi_list = MisiItem.objects.all().order_by('urutan', 'id')
    tujuan_list = TujuanItem.objects.all().order_by('urutan', 'id')

    context = {
        'visi_misi_obj': visi_misi_obj,
        'form_visi': form_visi,
        'form_misi': MisiItemForm(),
        'form_tujuan': TujuanItemForm(),
        'misi_list': misi_list,
        'tujuan_list': tujuan_list,
    }
    return render(request, 'landing/admin/dashboard_visi_misi_tujuan.html', context)


@login_required(login_url='landing:login')
@require_POST
def misi_create(request):
    form = MisiItemForm(request.POST)
    if form.is_valid():
        misi = form.save(commit=False)
        misi.visi_misi = VisiMisiTujuan.objects.first()
        misi.save()
        catat_log(request, request.user, f"Menambahkan Poin Misi Baru (Urutan {misi.urutan})", "Item misi berhasil ditambahkan")
        messages.success(request, f"Item Misi urutan ke-{misi.urutan} berhasil ditambahkan!")
    else:
        messages.error(request, "Gagal menambahkan item misi. Pastikan data terisi dengan benar.")
    return redirect('landing:dashboard_visi_misi_tujuan')


@login_required(login_url='landing:login')
@require_POST
def misi_update(request, pk):
    misi = get_object_or_404(MisiItem, pk=pk)
    form = MisiItemForm(request.POST, instance=misi)
    if form.is_valid():
        form.save()
        catat_log(request, request.user, f"Memperbarui Poin Misi (Urutan {misi.urutan})", "Item misi berhasil diperbarui")
        messages.success(request, f"Item Misi urutan ke-{misi.urutan} berhasil diperbarui!")
    else:
        messages.error(request, "Gagal memperbarui item misi.")
    return redirect('landing:dashboard_visi_misi_tujuan')


@login_required(login_url='landing:login')
@require_POST
def misi_delete(request, pk):
    misi = get_object_or_404(MisiItem, pk=pk)
    urutan = misi.urutan
    misi.delete()
    catat_log(request, request.user, f"Menghapus Poin Misi (Urutan {urutan})", "Item misi telah dihapus")
    messages.success(request, f"Item Misi urutan ke-{urutan} berhasil dihapus!")
    return redirect('landing:dashboard_visi_misi_tujuan')


@login_required(login_url='landing:login')
@require_POST
def tujuan_create(request):
    form = TujuanItemForm(request.POST)
    if form.is_valid():
        tujuan = form.save(commit=False)
        tujuan.visi_misi = VisiMisiTujuan.objects.first()
        tujuan.save()
        catat_log(request, request.user, f"Menambahkan Poin Tujuan Baru: '{tujuan.judul}'", "Item tujuan berhasil ditambahkan")
        messages.success(request, f"Item Tujuan '{tujuan.judul}' berhasil ditambahkan!")
    else:
        messages.error(request, "Gagal menambahkan item tujuan. Pastikan data terisi dengan benar.")
    return redirect('landing:dashboard_visi_misi_tujuan')


@login_required(login_url='landing:login')
@require_POST
def tujuan_update(request, pk):
    tujuan = get_object_or_404(TujuanItem, pk=pk)
    form = TujuanItemForm(request.POST, instance=tujuan)
    if form.is_valid():
        form.save()
        catat_log(request, request.user, f"Memperbarui Poin Tujuan: '{tujuan.judul}'", "Item tujuan berhasil diperbarui")
        messages.success(request, f"Item Tujuan '{tujuan.judul}' berhasil diperbarui!")
    else:
        messages.error(request, "Gagal memperbarui item tujuan.")
    return redirect('landing:dashboard_visi_misi_tujuan')


@login_required(login_url='landing:login')
@require_POST
def tujuan_delete(request, pk):
    tujuan = get_object_or_404(TujuanItem, pk=pk)
    judul = tujuan.judul
    tujuan.delete()
    catat_log(request, request.user, f"Menghapus Poin Tujuan: '{judul}'", "Item tujuan telah dihapus")
    messages.success(request, f"Item Tujuan '{judul}' berhasil dihapus!")
    return redirect('landing:dashboard_visi_misi_tujuan')


def detail_tentang(request, jenis):
    akreditasi = Akreditasi.objects.first()

    tentang_nav_list = [
        {
            'slug': 'profil',
            'title': 'Profil Program Studi',
            'subjudul': 'Profil lengkap Program Studi Sarjana (S1) Administrasi Publik FISIP Universitas Tadulako',
            'icon': 'fa-solid fa-university'
        },
        {
            'slug': 'sejarah',
            'title': 'Sejarah & Dasar Hukum',
            'subjudul': 'Tonggak sejarah pendirian dan landasan hukum operasional program studi',
            'icon': 'fa-solid fa-landmark'
        },
        {
            'slug': 'visi',
            'title': 'Visi, Misi & Tujuan',
            'subjudul': 'Arah strategis, komitmen mutu, dan capaian tujuan pendidikan',
            'icon': 'fa-solid fa-bullseye'
        },
        {
            'slug': 'profil-lulusan',
            'title': 'Profil Lulusan',
            'subjudul': 'Capaian kompetensi dan prospek karir profesional lulusan',
            'icon': 'fa-solid fa-user-graduate'
        },
        {
            'slug': 'sertifikat',
            'title': 'Sertifikat Akreditasi',
            'subjudul': 'Status peringkat akreditasi resmi program studi oleh BAN-PT',
            'icon': 'fa-solid fa-award'
        },
    ]

    # Normalisasi jenis slug
    jenis_clean = jenis.strip().lower().replace('_', '-')
    is_visi_misi_tujuan = jenis_clean in ['visimisi', 'visi-misi', 'misi', 'visi', 'tujuan']

    if is_visi_misi_tujuan:
        active_slug = 'visi'
        visi_misi_obj, _ = VisiMisiTujuan.objects.get_or_create(
            id=1,
            defaults={
                'visi': 'Menjadi Program Studi Administrasi Publik yang unggul secara global dan bereputasi nasional dalam pengembangan ilmu administrasi publik dan tata kelola pemerintahan yang adaptif, berintegritas, dan berwawasan lingkungan.',
                'pengantar_misi': 'Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki misi sebagai berikut:',
                'pengantar_tujuan': 'Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki tujuan Pendidikan berupa:'
            }
        )
        misi_list = MisiItem.objects.all().order_by('urutan', 'id')
        tujuan_list = TujuanItem.objects.all().order_by('urutan', 'id')
        konten_obj = TentangPage.objects.filter(slug='visi').first()
        target_section = 'tujuan' if jenis_clean == 'tujuan' else ('misi' if jenis_clean == 'misi' else 'visi')
        current_nav = next((item for item in tentang_nav_list if item['slug'] == 'visi'), None)
    else:
        if jenis_clean in ['profil-lulusan', 'profillulusan']:
            active_slug = 'profil-lulusan'
        elif jenis_clean in ['sejarah', 'sejarah-hukum']:
            active_slug = 'sejarah'
        elif jenis_clean in ['sertifikat', 'akreditasi']:
            active_slug = 'sertifikat'
        else:
            active_slug = 'profil'

        konten_obj = TentangPage.objects.filter(slug=active_slug).first()
        if not konten_obj:
            konten_obj = TentangPage.objects.filter(slug=jenis).first()
        visi_misi_obj = None
        misi_list = []
        tujuan_list = []
        target_section = None
        current_nav = next((item for item in tentang_nav_list if item['slug'] == active_slug), None)

    current_title = konten_obj.judul if konten_obj else (current_nav['title'] if current_nav else jenis.title())
    current_subjudul = current_nav['subjudul'] if current_nav else ''

    context = {
        'konten_obj': konten_obj,
        'active_slug': active_slug,
        'jenis': jenis,
        'akreditasi': akreditasi,
        'is_visi_misi_tujuan': is_visi_misi_tujuan,
        'visi_misi_obj': visi_misi_obj,
        'misi_list': misi_list,
        'tujuan_list': tujuan_list,
        'target_section': target_section,
        'tentang_nav_list': tentang_nav_list,
        'current_title': current_title,
        'current_subjudul': current_subjudul,
    }
    return render(request, 'landing/tentang_detail.html', context)


# ==============================================================================
# MENU AKADEMIK (PUBLIK & ADMIN PORTAL)
# ==============================================================================

def detail_akademik(request, slug):
    akademik_list = AkademikPage.objects.filter(is_active=True).order_by('urutan', 'id')
    current_page = get_object_or_404(AkademikPage, slug=slug, is_active=True)
    dokumen_list = current_page.dokumen_list.all().order_by('-uploaded_at')

    context = {
        'current_page': current_page,
        'akademik_list': akademik_list,
        'dokumen_list': dokumen_list,
    }
    return render(request, 'landing/akademik_detail.html', context)


@login_required(login_url='landing:login')
def dashboard_akademik(request):
    akademik_list = AkademikPage.objects.all().order_by('urutan', 'id')
    
    # Tentukan sub-menu yang sedang dipilih untuk diedit (dari ?edit=<id> atau item pertama)
    edit_id = request.GET.get('edit')
    selected_item = None
    if edit_id:
        selected_item = AkademikPage.objects.filter(pk=edit_id).first()
    if not selected_item and akademik_list.exists():
        selected_item = akademik_list.first()

    # Form untuk modal tambah sub-menu baru
    create_form = AkademikPageForm()

    # Proses update sub-menu yang sedang dipilih
    if request.method == 'POST' and 'update_akademik' in request.POST:
        target_id = request.POST.get('target_id')
        target_item = get_object_or_404(AkademikPage, pk=target_id)
        edit_form = AkademikPageForm(request.POST, request.FILES, instance=target_item)
        if edit_form.is_valid():
            edit_form.save()
            catat_log(request, request.user, f"Memperbarui Konten Sub-Menu Akademik: '{target_item.judul}'", "Konten akademik berhasil disimpan")
            messages.success(request, f"Konten sub-menu '{target_item.judul}' berhasil diperbarui!")
            return redirect(f"/admin-portal/akademik/?edit={target_item.pk}#editPanel")
        else:
            messages.error(request, "Terjadi kesalahan saat menyimpan formulir. Silakan periksa kembali.")
            selected_item = target_item
    else:
        edit_form = AkademikPageForm(instance=selected_item) if selected_item else None

    dokumen_list = selected_item.dokumen_list.all().order_by('-uploaded_at') if selected_item else []
    dokumen_form = DokumenAkademikForm()

    context = {
        'akademik_list': akademik_list,
        'selected_item': selected_item,
        'edit_form': edit_form,
        'create_form': create_form,
        'dokumen_list': dokumen_list,
        'dokumen_form': dokumen_form,
    }
    return render(request, 'landing/admin/dashboard_akademik.html', context)


@login_required(login_url='landing:login')
def dashboard_akademik_edit(request, pk):
    # Pengalihan langsung ke halaman terpadu dashboard_akademik
    return redirect(f"/admin-portal/akademik/?edit={pk}#editPanel")


@login_required(login_url='landing:login')
def akademik_create(request):
    if request.method == 'POST':
        form = AkademikPageForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            catat_log(request, request.user, f"Menambahkan Sub-Menu Akademik: '{item.judul}'", "Sub-menu akademik baru ditambahkan")
            messages.success(request, f"Sub-menu '{item.judul}' berhasil ditambahkan!")
            return redirect(f"/admin-portal/akademik/?edit={item.pk}#editPanel")
        else:
            messages.error(request, "Terjadi kesalahan saat menambahkan sub-menu. Pastikan data terisi dengan benar.")
    return redirect('landing:dashboard_akademik')


@login_required(login_url='landing:login')
@require_POST
def akademik_delete(request, pk):
    item = get_object_or_404(AkademikPage, pk=pk)
    judul = item.judul
    item.delete()
    catat_log(request, request.user, f"Menghapus Sub-Menu Akademik: '{judul}'", "Sub-menu akademik dihapus")
    messages.success(request, f"Sub-menu '{judul}' berhasil dihapus!")
    return redirect('landing:dashboard_akademik')


@login_required(login_url='landing:login')
@require_POST
def akademik_dokumen_add(request, pk):
    item = get_object_or_404(AkademikPage, pk=pk)
    form = DokumenAkademikForm(request.POST, request.FILES)
    if form.is_valid():
        dokumen = form.save(commit=False)
        dokumen.akademik = item
        dokumen.save()
        catat_log(request, request.user, f"Mengunggah Dokumen '{dokumen.judul}' pada sub-menu '{item.judul}'", "Dokumen lampiran berhasil diunggah")
        messages.success(request, f"Dokumen '{dokumen.judul}' berhasil ditambahkan!")
    else:
        messages.error(request, "Gagal mengunggah dokumen. Pastikan file terpilih dengan benar.")
    return redirect(f"/admin-portal/akademik/?edit={item.pk}#editPanel")


@login_required(login_url='landing:login')
@require_POST
def akademik_dokumen_delete(request, pk):
    dokumen = get_object_or_404(DokumenAkademik, pk=pk)
    akademik_id = dokumen.akademik.pk
    judul = dokumen.judul
    dokumen.delete()
    catat_log(request, request.user, f"Menghapus Dokumen Lampiran: '{judul}'", "Dokumen lampiran dihapus")
    messages.success(request, f"Dokumen '{judul}' berhasil dihapus!")
    return redirect(f"/admin-portal/akademik/?edit={akademik_id}#editPanel")



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Sambutan, Galeri, Berita, Akademik, TenagaPendidik, Akreditasi, Kontak 
from django.db.models import Q
from .forms import BeritaForm, LoginForm, TenagaPendidikForm
from django.contrib import messages
from django.core.paginator import Paginator
from akun.views import catat_log, catat_riwayat_login
from .forms import AdminUserCreateForm, AdminUserUpdateForm
from akun.models import RiwayatLogin, UserProfile
from .forms import CustomAuthenticationForm
from .forms import AdminUserForm
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
    akademik_list = Akademik.objects.all()
    return render(request, 'landing/akademik.html', {'akademik_list': akademik_list})

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
            catat_log(request.user, f"Menambahkan berita baru berjudul: '{berita.judul}'")
            
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
            catat_log(request.user, f"Mengubah berita berjudul: '{berita.judul}'")
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
        berita.delete()
        messages.success(request, "Data berita berhasil dihapus!")
        catat_log(request.user, f"Menghapus berita: '{berita.judul}'")
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
        # UBAH DARI slug=id_hapus MENJADI pk=id_hapus (karena model pakai ID)
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
            
            # ---> CATAT LOG TAMBAH TENDIK <---
            catat_log(request.user, f"Menambahkan data tendik baru: '{tendik_baru.nama}'")
            
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
            
            # ---> CATAT LOG EDIT TENDIK <---
            catat_log(request.user, f"Memperbarui data tendik: '{tendik.nama}'")
            
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
        nama_tendik = tendik.nama  # Simpan nama sebelum dihapus dari database
        tendik.delete()
        
        # ---> CATAT LOG HAPUS TENDIK <---
        catat_log(request.user, f"Menghapus data tendik: '{nama_tendik}'")
        
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
        email_input = request.POST.get('username')  # Karena input form menampung email/username
        password_input = request.POST.get('password')
        
        # Cari user berdasarkan email yang diinput
        try:
            user_obj = User.objects.get(email=email_input)
            username_asli = user_obj.username
        except User.DoesNotExist:
            username_asli = email_input  # Fallback kalau yang diinput ternyata langsung username-nya
            
        # Autentikasi menggunakan username asli & password
        user = authenticate(request, username=username_asli, password=password_input)
            
        if user is not None:
            login(request, user)
            
            # Catat riwayat login ke database secara otomatis
            catat_riwayat_login(user, request)
            
            messages.success(request, f"Selamat datang, {user.get_full_name() or user.username}!")
            
            # Cek role: Hanya admin/staff yang boleh masuk dashboard admin
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

from .models import Berita, TenagaPendidik, AuditLog  # Pastikan AuditLog di-import

@login_required(login_url='landing:login')
def dashboard_admin_khusus(request):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "Akses ditolak!")
        logout(request)
        return redirect('landing:login')
        
    berita_list = Berita.objects.all().order_by('-post_date')
    total_berita = berita_list.count()
    total_tendik = TenagaPendidik.objects.count() # Hitung total tendik
    
    # ---> AMBIL DATA AUDIT LOG DI SINI (Contoh ambil 10 aktivitas terbaru) <---
    logs = AuditLog.objects.all().order_by('-waktu')[:10]

    context = {
        'berita_list': berita_list,
        'total_berita': total_berita,
        'total_tendik': total_tendik,
        'logs': logs,  # ---> MASUKKAN KE DICTIONARY CONTEXT <---
    }
    return render(request, 'landing/admin/dashboard.html', context) # Sesuaikan path file HTML dashboard lu

def catat_log(user, aktivitas):
    AuditLog.objects.create(user=user, aktivitas=aktivitas)

@login_required(login_url='landing:login')
def manajemen_user_view(request):
    users = User.objects.all().order_by('-date_joined')
    riwayat_login = RiwayatLogin.objects.all().order_by('-waktu_login') # Ganti '-waktu' jika field di models.py beda (misal: -timestamp)
    
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
            form.save()
            messages.success(request, "Akun administrator baru berhasil ditambahkan!")
            return redirect('landing:manajemen_user')
    else:
        form = AdminUserCreateForm()
    
    return render(request, 'landing/User/user_form.html', {'form': form})

# 2. Pada fungsi edit user
@login_required(login_url='landing:login')
def user_update_view(request, pk):
    if not request.user.is_superuser:
        messages.error(request, "Akses ditolak!")
        return redirect('landing:manajemen_user')
        
    target_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            catat_log(request.user, f"Memperbarui akun administrator: '{target_user.username}'")
            messages.success(request, "Akun administrator berhasil diperbarui!")
            return redirect('landing:manajemen_user')
    else:
        form = AdminUserForm(instance=target_user)
        
    # ---> SESUAIKAN PATH FOLDER DI SINI <---
    return render(request, 'landing/User/user_form.html', {'form': form, 'target_user': target_user})

@login_required(login_url='landing:login')
def user_delete_view(request, pk):
    target_user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        # IMPLEMENTASI SOFT DELETE (Alih-alih target_user.delete())
        target_user.is_active = False
        target_user.save()
        
        catat_log(request.user, f"Melakukan soft delete / menonaktifkan akun: '{target_user.username}'")
        messages.success(request, "Akun berhasil dinonaktifkan (Soft Delete).")
        return redirect('landing:manajemen_user')
        
    return render(request, 'landing/User/user_confirm_delete.html', {'target_user': target_user})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Sambutan, Galeri, Berita, Akademik, TenagaPendidik, Akreditasi, Kontak 
from django.db.models import Q
from .forms import BeritaForm, LoginForm, TenagaPendidikForm
from django.contrib import messages
from akun.views import catat_log

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
            form.save()
            # Berikan notifikasi sukses
            messages.success(request, "Data berita berhasil ditambahkan!")
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
            form.save()
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
        tendik.delete()
        messages.success(request, "Data tenaga pendidik berhasil dihapus!")
        return redirect('landing:tenaga_pendidik')
    return redirect('landing:tenaga_pendidik')

def galeri_page(request):
    galeri_list = Galeri.objects.all()
    return render(request, 'landing/galeri.html', {'galeri_list': galeri_list})

def akreditasi_page(request):
    akreditasi = Akreditasi.objects.last()
    return render(request, 'landing/akreditasi.html', {'akreditasi': akreditasi})

# --- VIEW LOGIN BERDASARKAN EMAIL & ROLE ADMIN ---
def login_view(request):
    if request.method == 'POST':
        email_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        try:
            user_obj = User.objects.get(email=email_input)
            username_asli = user_obj.username
        except User.DoesNotExist:
            username_asli = None
            
        user = None
        if username_asli:
            user = authenticate(request, username=username_asli, password=password_input)
            
        if user is not None:
            login(request, user)
            messages.success(request, f"Selamat datang, {user.get_full_name() or user.username}!")
            
            # CEK ROLE: Jika Admin / Staff, arahkan ke Dashboard Admin buatan sendiri
            if user.is_superuser or user.is_staff:
                return redirect('landing:dashboard_admin') 
            else:
                messages.error(request, "Akun Anda bukan Admin! Tidak memiliki hak akses.")
                logout(request)
                return redirect('landing:login')
        else:
            messages.error(request, "Email atau password salah.")
            
    form = LoginForm()
    return render(request, 'landing/Login/login.html', {'form': form})
    if request.method == 'POST':
        email_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # Cari username berdasarkan email yang diinput di form
        try:
            user_obj = User.objects.get(email=email_input)
            username_asli = user_obj.username
        except User.DoesNotExist:
            username_asli = None
            
        # Lakukan autentikasi menggunakan username asli yang terikat pada email tersebut
        user = None
        if username_asli:
            user = authenticate(request, username=username_asli, password=password_input)
            
        if user is not None:
            login(request, user)
            messages.success(request, f"Selamat datang, {user.get_full_name() or user.username}!")
            
            # Pengecekan role sesuai instruksi mentor: Jika ADMIN masuk ke dashboard, jika bukan ditolak
            if user.is_superuser or user.is_staff:
                return redirect('/admin/') 
            else:
                messages.error(request, "Akun Anda bukan Admin! Tidak memiliki hak akses.")
                logout(request)
                return redirect('landing:login')
        else:
            messages.error(request, "Email atau password salah.")
            
    form = LoginForm()
    return render(request, 'landing/Login/login.html', {'form': form})

@login_required(login_url='landing:login')
def dashboard_admin_khusus(request):
    if not (request.user.is_superuser or request.user.is_staff):
        messages.error(request, "Akses ditolak!")
        logout(request)
        return redirect('landing:login')
        
    berita_list = Berita.objects.all().order_by('-post_date')
    total_berita = berita_list.count()
    total_tendik = TenagaPendidik.objects.count() # Hitung total tendik

    context = {
        'berita_list': berita_list,
        'total_berita': total_berita,
        'total_tendik': total_tendik,
    }
    return render(request, 'landing/admin/dashboard.html', context)



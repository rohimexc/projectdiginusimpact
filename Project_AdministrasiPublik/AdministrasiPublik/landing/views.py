from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Sambutan, Galeri, Berita, Akademik, TenagaPendidik, Akreditasi, Kontak 
from django.db.models import Q
from .forms import BeritaForm, LoginForm

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
    return render(request, 'landing/berita_list.html', context)

# 2. Halaman Detail (Single Berita saat "Baca Selengkapnya" diklik)
def berita_detail_view(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    return render(request, 'landing/berita_detail.html', {'berita': berita})

# 3. Create Berita (Tambah)
@login_required(login_url='/admin/login/')
def berita_create_view(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('berita_list')
    else:
        form = BeritaForm()
    return render(request, 'landing/berita_form.html', {'form': form})

# 4. Update Berita (Edit)
@login_required(login_url='/admin/login/')
def berita_update_view(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    if request.method == 'POST':
        form = BeritaForm(request.POST, request.FILES, instance=berita)
        if form.is_valid():
            form.save()
            return redirect('berita_list')
    else:
        form = BeritaForm(instance=berita)
    return render(request, 'landing/berita_form.html', {'form': form, 'berita': berita})

# 5. Delete Berita (Hapus)
@login_required(login_url='/admin/login/')
def berita_delete_view(request, slug):
    berita = get_object_or_404(Berita, slug=slug)
    if request.method == 'POST':
        berita.delete()
        return redirect('berita_list')
    return render(request, 'landing/berita_confirm_delete.html', {'berita': berita})

def tenaga_pendidik_view(request):
    query = request.GET.get('q', '')
    if query:
        # Filter berdasarkan nama, bidang ilmu, atau NIP menggunakan Q
        pendidik_list = TenagaPendidik.objects.filter(
            Q(nama__icontains=query) | 
            Q(bidang_ilmu__icontains=query) | 
            Q(nip__icontains=query)
        )
    else:
        pendidik_list = TenagaPendidik.objects.all()

    context = {
        'pendidik_list': pendidik_list,
        'query': query,
    }
    return render(request, 'landing/TenagaPendidik/Tenaga_Pendidik.html', context)

def detail_tenaga_pendidik_view(request, pk):
    pendidik = get_object_or_404(TenagaPendidik, pk=pk)
    context = {
        'pendidik': pendidik,
    }
    return render(request, 'landing/TenagaPendidik/detail_tenaga_pendidik.html', context)

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

# --- VIEW TERPROTEKSI ---
@login_required(login_url='/admin/login/')
def dashboard_admin_khusus(request):
    if not request.user.is_staff:
        return render(request, 'landing/403.html', status=403)
    return render(request, 'landing/dashboard.html')
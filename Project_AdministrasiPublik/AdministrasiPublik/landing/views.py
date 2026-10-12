from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Sambutan, Galeri, Berita, Akademik, StafDosen, Akreditasi, Kontak
from .forms import BeritaForm
def index(request):
    berita_list = Berita.objects.all().order_by('-post_date')[:3] # Ambil 3 berita terbaru
    galeri_list = Galeri.objects.all()
    akademik_list = Akademik.objects.all()
    staf_list = StafDosen.objects.all()
    akreditasi = Akreditasi.objects.first()
    kontak = Kontak.objects.first()
    sambutan = Sambutan.objects.first()

    context = {
        'berita_list': berita_list, # <-- Pastikan variabel ini ada di sini
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

def staf_page(request):
    staf_list = StafDosen.objects.all()
    return render(request, 'landing/staf.html', {'staf_list': staf_list})

def galeri_page(request):
    galeri_list = Galeri.objects.all()
    return render(request, 'landing/galeri.html', {'galeri_list': galeri_list})

def akreditasi_page(request):
    akreditasi = Akreditasi.objects.last()
    return render(request, 'landing/akreditasi.html', {'akreditasi': akreditasi})

# --- CONTOH VIEW TERPROTEKSI (Hanya untuk User yang Login / Admin) ---
@login_required(login_url='/admin/login/')
def dashboard_admin_khusus(request):
    # Pastikan hanya user yang berstatus staff atau superuser yang bisa masuk
    if not request.user.is_staff:
        return render(request, 'landing/403.html', status=403) # Atau redirect ke halaman lain
    return render(request, 'landing/dashboard.html')
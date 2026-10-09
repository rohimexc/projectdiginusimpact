from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Sambutan, Galeri, Berita, Akademik, StafDosen, Akreditasi, Kontak

def index(request):
    return render(request, 'landing/index.html')

def tentang(request):
    sambutan = Sambutan.objects.last()
    return render(request, 'landing/tentang.html', {'sambutan': sambutan})

def akademik(request):
    akademik_list = Akademik.objects.all()
    return render(request, 'landing/akademik.html', {'akademik_list': akademik_list})

def berita_page(request):
    berita_list = Berita.objects.all()
    return render(request, 'landing/berita.html', {'berita_list': berita_list})

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
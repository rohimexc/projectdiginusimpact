from django.shortcuts import render
from .models import Sambutan, Galeri, Berita

# View untuk menampilkan halaman utama (landing page) dan mengambil data dari database
def home(request):
    sambutan = Sambutan.objects.first()
    daftar_galeri = Galeri.objects.all()
    daftar_berita = Berita.objects.all()

    context = {
        'sambutan': sambutan,
        'daftar_galeri': daftar_galeri,
        'daftar_berita': daftar_berita,
    }
    return render(request, 'core/index.html', context)
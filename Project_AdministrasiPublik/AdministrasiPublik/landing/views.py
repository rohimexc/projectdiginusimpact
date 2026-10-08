from django.shortcuts import render
from .models import Sambutan, Galeri, Berita, Akademik, StafDosen, Akreditasi, Kontak

def index(request):
    sambutan = Sambutan.objects.last()
    galeri_list = Galeri.objects.all()
    berita_list = Berita.objects.all()
    akademik_list = Akademik.objects.all()
    staf_list = StafDosen.objects.all()
    akreditasi = Akreditasi.objects.last()
    kontak = Kontak.objects.last()

    context = {
        'title': 'Program Studi Administrasi Publik',
        'faculty': 'Fakultas Ilmu Sosial dan Ilmu Politik',
        'sambutan': sambutan,
        'galeri_list': galeri_list,
        'berita_list': berita_list,
        'akademik_list': akademik_list,
        'staf_list': staf_list,
        'akreditasi': akreditasi,
        'kontak': kontak,
    }
    return render(request, 'landing/index.html', context)
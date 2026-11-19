from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Selamat Datang di Halaman Kontak',
        'content': 'Di Belajar DJANGO',
        'kontak': 'kontak/images/logo.png',
    }
    return render(request, 'kontak/index.html', context)
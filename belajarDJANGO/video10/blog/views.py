from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Selamat Datang di Halaman BLOG',
        'content': 'Di Belajar DJANGO',
    }
    return render(request, 'blog/index.html', context)

def Artikel(request):
    context = {
        'title': 'Artikel',
        'content': 'Ini adalah halaman artikel',
    }
    return render(request, 'blog/index.html', context)

def Berita(request):
    context = {
        'title': 'Berita',
        'content': 'Ini adalah halaman berita',
    }
    return render(request, 'blog/index.html', context)
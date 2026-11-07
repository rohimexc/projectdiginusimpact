from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Selamat Datang di Halaman BLOG',
        'content': 'Di Belajar DJANGO',
        'nav':[
            ['/','blog'],
            ['/blog/artikel','artikel'],
            ['/blog/berita','berita'],
        ]
    }
    return render(request, 'blog/index.html', context)
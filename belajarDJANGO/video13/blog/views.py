from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Selamat Datang di Halaman BLOG',
        'content': 'Di Belajar DJANGO',
        'blog': 'blog/images/anjing.png',
    }
    return render(request, 'blog/index.html', context)
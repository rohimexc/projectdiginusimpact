from django.shortcuts import render

def index(request):
    context = {
        'title': 'Selamat Datang',
        'content': 'Di Belajar DJANGO',
    }
    return render(request, 'index.html', context)
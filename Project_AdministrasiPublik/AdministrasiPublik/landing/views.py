from django.shortcuts import render


def index(request):
    context = {
        'title': 'Program Studi Ilmu Administrasi Publik',
        'faculty': 'Fakultas Ilmu Sosial dan Ilmu Politik',
        'vision': 'Menjadi program studi unggul dalam pengembangan tata kelola publik yang inovatif, cerdas, dan berintegritas.',
    }
    return render(request, 'landing/index.html', context)
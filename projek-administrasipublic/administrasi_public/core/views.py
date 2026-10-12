from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Sambutan, Galeri, Berita
from .forms import BeritaForm

# 1. View Halaman Utama (Landing Page)
def home(request):
    sambutan = Sambutan.objects.first()
    daftar_galeri = Galeri.objects.all()[:6]
    # Ambil 3 berita terbaru yang diurutkan dari posted_at
    daftar_berita = Berita.objects.all().order_by('-posted_at')[:3]

    context = {
        'sambutan': sambutan,
        'daftar_galeri': daftar_galeri,
        'daftar_berita': daftar_berita,
    }
    return render(request, 'core/index.html', context)


# 2. View Daftar Semua Berita (Search, Filter Tanggal/Bulan/Tahun, Pagination)
def berita_list(request):
    query = request.GET.get('q', '')
    tahun = request.GET.get('tahun', '')
    bulan = request.GET.get('bulan', '')
    tanggal = request.GET.get('tanggal', '')

    berita_qs = Berita.objects.all().order_by('-posted_at')

    # Fitur Search
    if query:
        berita_qs = berita_qs.filter(
            Q(judul__icontains=query) | Q(konten__icontains=query) | Q(ringkasan__icontains=query)
        )

    # Fitur Filter Waktu
    if tahun:
        berita_qs = berita_qs.filter(posted_at__year=tahun)
    if bulan:
        berita_qs = berita_qs.filter(posted_at__month=bulan)
    if tanggal:
        berita_qs = berita_qs.filter(posted_at__date=tanggal)

    # Pagination 9 berita per halaman
    paginator = Paginator(berita_qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
        'selected_tahun': tahun,
        'selected_bulan': bulan,
        'selected_tanggal': tanggal,
    }
    return render(request, 'core/Berita/list.html', context)


# 3. View Detail Single Berita
def berita_detail(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    berita_terkait = Berita.objects.exclude(pk=pk).order_by('-posted_at')[:3]
    return render(request, 'core/Berita/detail.html', {'berita': berita, 'berita_terkait': berita_terkait})


# 4. View Tambah Berita (Create)
def berita_create(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('berita_list')
    else:
        form = BeritaForm()
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Tambah Berita Baru'})


# 5. View Edit Berita (Update)
def berita_update(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        form = BeritaForm(request.POST, instance=berita)
        if form.is_valid():
            form.save()
            return redirect('berita_detail', pk=berita.pk)
    else:
        form = BeritaForm(instance=berita)
    return render(request, 'core/berita/form.html', {'form': form, 'title': 'Edit Berita'})


# 6. View Hapus Berita (Delete)
def berita_delete(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        berita.delete()
        return redirect('berita_list')
    return render(request, 'core/berita/delete_confirm.html', {'berita': berita})
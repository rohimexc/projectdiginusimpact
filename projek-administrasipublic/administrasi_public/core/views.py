from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Sambutan, Galeri, Berita, TenagaPendidik
from .forms import BeritaForm, TenagaPendidikForm

# ==========================================
# 1. LANDING PAGE & BERITA
# ==========================================

# View Halaman Utama (Landing Page)
def home(request):
    sambutan = Sambutan.objects.first()
    daftar_galeri = Galeri.objects.all()[:6]
    daftar_berita = Berita.objects.all().order_by('-posted_at')[:3]
    # Ambil 3 tenaga kependidikan untuk ditampilkan di seksi Beranda
    daftar_tenaga_kependidikan = TenagaPendidik.objects.all()[:3]

    context = {
        'sambutan': sambutan,
        'daftar_galeri': daftar_galeri,
        'daftar_berita': daftar_berita,
        'daftar_tenaga_kependidikan': daftar_tenaga_kependidikan,
    }
    return render(request, 'core/index.html', context)


# View Daftar Semua Berita (Search, Filter, Pagination)
def berita_list(request):
    query = request.GET.get('q', '')
    tahun = request.GET.get('tahun', '')
    bulan = request.GET.get('bulan', '')
    tanggal = request.GET.get('tanggal', '')

    berita_qs = Berita.objects.all().order_by('-posted_at')

    if query:
        berita_qs = berita_qs.filter(
            Q(judul__icontains=query) | Q(konten__icontains=query) | Q(ringkasan__icontains=query)
        )

    if tahun:
        berita_qs = berita_qs.filter(posted_at__year=tahun)
    if bulan:
        berita_qs = berita_qs.filter(posted_at__month=bulan)
    if tanggal:
        berita_qs = berita_qs.filter(posted_at__date=tanggal)

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


# View Detail Single Berita
def berita_detail(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    berita_terkait = Berita.objects.exclude(pk=pk).order_by('-posted_at')[:3]
    return render(request, 'core/Berita/detail.html', {'berita': berita, 'berita_terkait': berita_terkait})


# View Tambah Berita (Create)
def berita_create(request):
    if request.method == 'POST':
        form = BeritaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('berita_list')
    else:
        form = BeritaForm()
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Tambah Berita Baru'})


# View Edit Berita (Update)
def berita_update(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        form = BeritaForm(request.POST, instance=berita)
        if form.is_valid():
            form.save()
            return redirect('berita_detail', pk=berita.pk)
    else:
        form = BeritaForm(instance=berita)
    return render(request, 'core/Berita/form.html', {'form': form, 'title': 'Edit Berita'})


# View Hapus Berita (Delete)
def berita_delete(request, pk):
    berita = get_object_or_404(Berita, pk=pk)
    if request.method == 'POST':
        berita.delete()
        return redirect('berita_list')
    return render(request, 'core/Berita/delete_confirm.html', {'berita': berita})


# ==========================================
# 2. TENAGA KEPENDIDIKAN
# ==========================================

# View Halaman Katalog Tenaga Kependidikan (Search Nama/Bidang/NIDN)
def tenaga_kependidikan_list(request):
    query = request.GET.get('q', '')
    kependidikan_qs = TenagaPendidik.objects.all().order_by('nama')

    if query:
        kependidikan_qs = kependidikan_qs.filter(
            Q(nama__icontains=query) |
            Q(bidang_ilmu__icontains=query) |
            Q(nidn__icontains=query)
        )

    context = {
        'tenaga_kependidikan_list': kependidikan_qs,
        'query': query,
    }
    return render(request, 'core/kependidikan/list.html', context)


# View Detail Tenaga Kependidikan
def tenaga_kependidikan_detail(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    tenaga_kependidikan_lainnya = TenagaPendidik.objects.exclude(pk=pk)[:3]
    context = {
        'tenaga_kependidikan': tenaga_kependidikan,
        'tenaga_kependidikan_lainnya': tenaga_kependidikan_lainnya,
    }
    return render(request, 'core/kependidikan/detail.html', context)


# View Tambah Tenaga Kependidikan (Create)
def tenaga_kependidikan_create(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tenaga_kependidikan_list')
    else:
        form = TenagaPendidikForm()
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Tambah Tenaga Kependidikan'})


# View Edit Tenaga Kependidikan (Update)
def tenaga_kependidikan_update(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=tenaga_kependidikan)
        if form.is_valid():
            form.save()
            return redirect('tenaga_kependidikan_list')
    else:
        form = TenagaPendidikForm(instance=tenaga_kependidikan)
    return render(request, 'core/kependidikan/form.html', {'form': form, 'title': 'Edit Tenaga Kependidikan'})


# View Hapus Tenaga Kependidikan (Delete)
def tenaga_kependidikan_delete(request, pk):
    tenaga_kependidikan = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        tenaga_kependidikan.delete()
        return redirect('tenaga_kependidikan_list')
    return render(request, 'core/kependidikan/delete_confirm.html', {'tenaga_kependidikan': tenaga_kependidikan})
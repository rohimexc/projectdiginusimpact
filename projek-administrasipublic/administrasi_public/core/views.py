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
    # Ambil 3 tenaga pendidik untuk ditampilkan di seksi Beranda
    daftar_dosen = TenagaPendidik.objects.all()[:3]

    context = {
        'sambutan': sambutan,
        'daftar_galeri': daftar_galeri,
        'daftar_berita': daftar_berita,
        'daftar_dosen': daftar_dosen,
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
# 2. TENAGA PENDIDIK / STAF DOSEN
# ==========================================

# View Halaman Katalog Tenaga Pendidik (Search Dosen/Bidang/NIDN)
def tenaga_pendidik_list(request):
    query = request.GET.get('q', '')
    dosen_qs = TenagaPendidik.objects.all().order_by('nama')

    if query:
        dosen_qs = dosen_qs.filter(
            Q(nama__icontains=query) |
            Q(bidang_ilmu__icontains=query) |
            Q(nidn__icontains=query)
        )

    context = {
        'dosen_list': dosen_qs,
        'query': query,
    }
    return render(request, 'core/dosen/list.html', context)


# View Detail Tenaga Pendidik (Klik "Lihat Selengkapnya")
def dosen_detail(request, pk):
    dosen = get_object_or_404(TenagaPendidik, pk=pk)
    dosen_lainnya = TenagaPendidik.objects.exclude(pk=pk)[:3]
    context = {
        'dosen': dosen,
        'dosen_lainnya': dosen_lainnya,
    }
    return render(request, 'core/dosen/detail.html', context)


# View Tambah Tenaga Pendidik (Create)
def dosen_create(request):
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tenaga_pendidik_list')
    else:
        form = TenagaPendidikForm()
    return render(request, 'core/dosen/form.html', {'form': form, 'title': 'Tambah Tenaga Pendidik'})


# View Edit Tenaga Pendidik (Update)
def dosen_update(request, pk):
    dosen = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        form = TenagaPendidikForm(request.POST, request.FILES, instance=dosen)
        if form.is_valid():
            form.save()
            return redirect('tenaga_pendidik_list')
    else:
        form = TenagaPendidikForm(instance=dosen)
    return render(request, 'core/dosen/form.html', {'form': form, 'title': 'Edit Tenaga Pendidik'})


# View Hapus Tenaga Pendidik (Delete)
def dosen_delete(request, pk):
    dosen = get_object_or_404(TenagaPendidik, pk=pk)
    if request.method == 'POST':
        dosen.delete()
        return redirect('tenaga_pendidik_list')
    return render(request, 'core/dosen/delete_confirm.html', {'dosen': dosen})
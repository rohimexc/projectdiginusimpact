from django.contrib import admin
from .models import Sambutan, Galeri, Berita

@admin.register(Sambutan)
class SambutanAdmin(admin.ModelAdmin):
    # Kolom yang ditampilkan pada tabel data
    list_display = ('judul', 'nama_author', 'foto')
    
    # 1. Search bar (cari berdasarkan judul, nama author, atau isi sambutan)
    search_fields = ('judul', 'nama_author', 'isi')
    
    # 2. Filter di sidebar kanan
    list_filter = ('nama_author',)
    
    # 3. Sort default berdasarkan ID terbaru
    ordering = ('-id',)


@admin.register(Galeri)
class GaleriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'gambar')
    
    # 1. Search bar
    search_fields = ('judul',)
    
    # 2. Filter di sidebar kanan (karena cuma ada judul & gambar, filter berdasarkan judul)
    list_filter = ('judul',)
    
    # 3. Sort default berdasarkan ID terbaru
    ordering = ('-id',)


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal', 'gambar')
    
    # 1. Search bar
    search_fields = ('judul', 'ringkasan')
    
    # 2. Filter di sidebar kanan (bisa filter berdasarkan tanggal publikasi)
    list_filter = ('tanggal',)
    
    # 3. Sort default (berita tanggal terbaru paling atas)
    ordering = ('-tanggal',)
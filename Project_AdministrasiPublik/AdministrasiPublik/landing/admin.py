from django.contrib import admin
from .models import (
    Sambutan, Galeri, Berita, Akademik, 
    TenagaPendidik, Dosen, Akreditasi, Kontak, TentangPage
)


@admin.register(TentangPage)
class TentangPageAdmin(admin.ModelAdmin):
    list_display = ('judul', 'slug', 'updated_at')
    search_fields = ('judul', 'slug')
    prepopulated_fields = {'slug': ('judul',)}


@admin.register(Sambutan)
class SambutanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'nama_koor')
    search_fields = ('judul', 'nama_koor', 'isi_sambutan')

@admin.register(Galeri)
class GaleriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal')
    list_filter = ('tanggal',)
    search_fields = ('judul',)
    ordering = ('-tanggal',)

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'post_date')  # 'tanggal' diganti 'post_date'
    list_filter = ('post_date',)           # 'tanggal' diganti 'post_date'
    search_fields = ('judul', 'konten')
    ordering = ('-post_date',)             # 'tanggal' diganti 'post_date'

@admin.register(Akademik)
class AkademikAdmin(admin.ModelAdmin):
    list_display = ('judul_informasi',)
    search_fields = ('judul_informasi', 'deskripsi')

@admin.register(TenagaPendidik)
class TenagaPendidikAdmin(admin.ModelAdmin):
    # Sesuaikan dengan nama field baru di models.py
    list_display = ('nama', 'jk', 'kategori', 'status', 'pangkat', 'nip') 
    search_fields = ('nama', 'nip', 'email')

@admin.register(Akreditasi)
class AkreditasiAdmin(admin.ModelAdmin):
    list_display = ('status_akreditasi', 'nomor_sk', 'tanggal_kadaluarsa')
    list_filter = ('status_akreditasi',)

@admin.register(Kontak)
class KontakAdmin(admin.ModelAdmin):
    list_display = ('email', 'telepon')
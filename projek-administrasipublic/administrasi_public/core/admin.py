from django.contrib import admin
from .models import Sambutan, Galeri, Berita, TenagaPendidik
from .models import HalamanTentang

@admin.register(Sambutan)
class SambutanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'nama_author', 'foto')
    search_fields = ('judul', 'nama_author', 'isi')
    list_filter = ('nama_author',)
    ordering = ('-id',)


@admin.register(Galeri)
class GaleriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'gambar')
    search_fields = ('judul',)
    list_filter = ('judul',)
    ordering = ('-id',)


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'posted_at', 'created_at')
    search_fields = ('judul', 'ringkasan', 'konten')
    list_filter = ('posted_at', 'created_at')
    ordering = ('-posted_at',)


@admin.register(TenagaPendidik)
class TenagaPendidikAdmin(admin.ModelAdmin):
    list_display = ('nama', 'bidang_ilmu', 'status', 'nidn', 'email')
    search_fields = ('nama', 'bidang_ilmu', 'nidn', 'nip')
    list_filter = ('status', 'bidang_ilmu')
    ordering = ('nama',)
    
@admin.register(HalamanTentang)
class HalamanTentangAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'updated_at')
    list_filter = ('kategori',)
    search_fields = ('judul', 'isi')
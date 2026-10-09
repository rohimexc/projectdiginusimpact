from django.contrib import admin
from .models import Sambutan, Galeri, Berita, Akademik, StafDosen, Akreditasi, Kontak

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
    list_display = ('judul', 'tanggal')
    list_filter = ('tanggal',)
    search_fields = ('judul', 'konten')
    ordering = ('-tanggal',)

@admin.register(Akademik)
class AkademikAdmin(admin.ModelAdmin):
    list_display = ('judul_informasi',)
    search_fields = ('judul_informasi', 'deskripsi')

@admin.register(StafDosen)
class StafDosenAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jabatan', 'nip_nidn')
    list_filter = ('jabatan',)
    search_fields = ('nama', 'nip_nidn', 'jabatan')
    ordering = ('nama',)

@admin.register(Akreditasi)
class AkreditasiAdmin(admin.ModelAdmin):
    list_display = ('status_akreditasi', 'nomor_sk', 'tanggal_kadaluarsa')
    list_filter = ('status_akreditasi',)

@admin.register(Kontak)
class KontakAdmin(admin.ModelAdmin):
    list_display = ('email', 'telepon')
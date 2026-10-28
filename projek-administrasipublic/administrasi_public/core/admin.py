from django.contrib import admin
from .models import (
    Sambutan, 
    Galeri, 
    Berita, 
    TenagaPendidik, 
    HalamanTentang, 
    VisiMisiTujuan, 
    MisiItem, 
    TujuanItem,
    HalamanAkademik,
    DokumenAkademik
)

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


# ==========================================
# ADMIN BAWAAN DJANGO: VISI, MISI & TUJUAN
# ==========================================

class MisiItemInline(admin.TabularInline):
    model = MisiItem
    extra = 1
    fields = ('urutan', 'isi')
    ordering = ('urutan',)


class TujuanItemInline(admin.StackedInline):
    model = TujuanItem
    extra = 1
    fields = ('urutan', 'judul', 'subjudul', 'deskripsi')
    ordering = ('urutan',)


@admin.register(VisiMisiTujuan)
class VisiMisiTujuanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    fieldsets = (
        ('1. Visi Program Studi', {
            'fields': ('visi_teks',),
            'description': 'Teks pernyataan visi utama Program Studi.'
        }),
        ('2. Pengantar Misi & Tujuan', {
            'fields': ('misi_intro', 'tujuan_intro'),
            'description': 'Kalimat pengantar yang muncul di atas daftar kartu Misi dan Tujuan.'
        }),
    )
    inlines = [MisiItemInline, TujuanItemInline]


@admin.register(MisiItem)
class MisiItemAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'isi')
    list_display_links = ('isi',)
    list_editable = ('urutan',)
    ordering = ('urutan',)
    search_fields = ('isi',)


@admin.register(TujuanItem)
class TujuanItemAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'judul', 'subjudul', 'deskripsi')
    list_display_links = ('judul',)
    list_editable = ('urutan',)
    ordering = ('urutan',)
    search_fields = ('judul', 'subjudul', 'deskripsi')


# ==========================================
# ADMIN BAWAAN DJANGO: MENU AKADEMIK
# (SIGA-8, Kurikulum, Jadwal, RPS, Panduan)
# ==========================================

class DokumenAkademikInline(admin.TabularInline):
    model = DokumenAkademik
    extra = 1
    fields = ('judul', 'file', 'keterangan')


@admin.register(HalamanAkademik)
class HalamanAkademikAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'link_eksternal', 'file_utama', 'updated_at')
    list_filter = ('kategori',)
    search_fields = ('judul', 'subjudul', 'isi')
    fieldsets = (
        ('Identitas Halaman Akademik', {
            'fields': ('kategori', 'judul', 'subjudul')
        }),
        ('Isi & Konten Lengkap', {
            'fields': ('isi',),
            'description': 'Gunakan editor rich-text untuk menyusun penjelasan akademik.'
        }),
        ('Tautan Eksternal & Dokumen Utama', {
            'fields': ('link_eksternal', 'file_utama', 'nama_file_utama'),
            'description': 'Tautan portal luar (misal: Portal SIGA-8) dan dokumen unduhan utama.'
        }),
    )
    inlines = [DokumenAkademikInline]


@admin.register(DokumenAkademik)
class DokumenAkademikAdmin(admin.ModelAdmin):
    list_display = ('judul', 'halaman', 'file', 'uploaded_at')
    list_filter = ('halaman__kategori',)
    search_fields = ('judul', 'keterangan')
    ordering = ('-uploaded_at',)

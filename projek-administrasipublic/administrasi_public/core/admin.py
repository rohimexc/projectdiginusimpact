from django.contrib import admin
from django.utils.html import format_html
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
    DokumenAkademik,
    Pengunjung,
    PengunjungTotal,
    Event
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
    list_display = ('nama', 'jenis', 'jabatan_fungsional', 'bidang_ilmu', 'status', 'nidn', 'email')
    search_fields = ('nama', 'bidang_ilmu', 'nidn', 'nip')
    list_filter = ('jenis', 'jabatan_fungsional', 'status', 'bidang_ilmu')
    ordering = ('nama',)

    
@admin.register(HalamanTentang)
class HalamanTentangAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'gambar', 'updated_at')
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


@admin.register(Pengunjung)
class PengunjungAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'tanggal', 'created_at', 'session_key')
    list_filter = ('tanggal',)
    search_fields = ('ip_address', 'session_key')
    ordering = ('-created_at',)
    readonly_fields = ('ip_address', 'session_key', 'user_agent', 'path', 'tanggal', 'created_at')


@admin.register(PengunjungTotal)
class PengunjungTotalAdmin(admin.ModelAdmin):
    list_display = ('total_awal', 'hari_ini_awal', 'updated_at')


# ==========================================
# ADMIN BAWAAN DJANGO: EVENT / AGENDA TERDEKAT
# ==========================================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('poster_thumbnail', 'judul', 'kategori', 'tanggal_mulai', 'waktu', 'lokasi', 'is_active', 'created_at')
    list_display_links = ('judul',)
    list_filter = ('is_active', 'kategori', 'tanggal_mulai')
    search_fields = ('judul', 'lokasi', 'kategori', 'deskripsi')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('judul',)}
    date_hierarchy = 'tanggal_mulai'
    ordering = ('tanggal_mulai', '-created_at')

    def poster_thumbnail(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="width: 48px; height: 60px; object-fit: cover; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);" title="{}" />',
                obj.poster.url,
                obj.judul
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px; font-style: italic;">Tanpa Poster</span>')
    poster_thumbnail.short_description = 'Poster (4:5)'


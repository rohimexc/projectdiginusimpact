from django.contrib import admin
from .models import (
    Sambutan, Galeri, Berita, Akademik, 
    TenagaPendidik, Dosen, Akreditasi, Kontak, TentangPage,
    VisiMisiTujuan, MisiItem, TujuanItem,
    AkademikPage, DokumenAkademik
)


class MisiItemInline(admin.TabularInline):
    model = MisiItem
    extra = 1
    fields = ('urutan', 'deskripsi')


class TujuanItemInline(admin.TabularInline):
    model = TujuanItem
    extra = 1
    fields = ('urutan', 'judul', 'subjudul', 'deskripsi')


@admin.register(VisiMisiTujuan)
class VisiMisiTujuanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    inlines = [MisiItemInline, TujuanItemInline]


@admin.register(MisiItem)
class MisiItemAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'deskripsi')
    ordering = ('urutan',)


@admin.register(TujuanItem)
class TujuanItemAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'judul', 'subjudul')
    ordering = ('urutan',)


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


class DokumenAkademikInline(admin.TabularInline):
    model = DokumenAkademik
    extra = 1
    fields = ('judul', 'file', 'keterangan')


@admin.register(AkademikPage)
class AkademikPageAdmin(admin.ModelAdmin):
    list_display = ('urutan', 'judul', 'slug', 'link_eksternal', 'file_utama', 'is_active', 'updated_at')
    list_display_links = ('judul',)
    list_editable = ('urutan', 'is_active')
    search_fields = ('judul', 'slug', 'subjudul')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('judul',)}
    inlines = [DokumenAkademikInline]


@admin.register(DokumenAkademik)
class DokumenAkademikAdmin(admin.ModelAdmin):
    list_display = ('judul', 'akademik', 'file', 'uploaded_at')
    list_filter = ('akademik',)
    search_fields = ('judul', 'keterangan')

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
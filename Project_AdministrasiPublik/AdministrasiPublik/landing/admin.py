from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    Sambutan, Galeri, Berita, Akademik, 
    TenagaPendidik, Dosen, Akreditasi, Kontak, TentangPage,
    VisiMisiTujuan, MisiItem, TujuanItem,
    AkademikPage, DokumenAkademik, LikeBerita, KomentarBerita,
    Hero
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
    list_display = ('foto_preview', 'urutan', 'aksi', 'judul', 'tanggal')
    list_editable = ('urutan',)
    list_filter = ('tanggal',)
    search_fields = ('judul',)
    ordering = ('urutan', '-tanggal', '-id')

    def foto_preview(self, obj):
        if obj.foto:
            return mark_safe(f'<a href="{obj.foto.url}" target="_blank"><img src="{obj.foto.url}" width="60" height="45" style="object-fit:cover; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.2);" title="Klik untuk preview" /></a>')
        return "-"
    foto_preview.short_description = "Foto"

    def aksi(self, obj):
        from django.urls import reverse
        change_url = reverse('admin:landing_galeri_change', args=[obj.id])
        delete_url = reverse('admin:landing_galeri_delete', args=[obj.id])
        preview_tag = f'<a href="{obj.foto.url}" target="_blank" style="margin-right:8px; font-weight:600; color:#0f6b6b;" title="Preview">Preview</a>' if obj.foto else ''
        return mark_safe(f'{preview_tag}<a href="{change_url}" style="margin-right:8px; font-weight:600; color:#d97706;">Edit</a><a href="{delete_url}" style="font-weight:600; color:#dc2626;">Hapus</a>')
    aksi.short_description = "Aksi"


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('video_url_display', 'foto_preview', 'aksi', 'judul', 'is_active')
    list_editable = ('is_active',)
    search_fields = ('judul', 'subjudul', 'video_url')
    list_filter = ('is_active', 'updated_at')

    def video_url_display(self, obj):
        return obj.video_url or "-"
    video_url_display.short_description = "Link Video"

    def foto_preview(self, obj):
        if obj.foto:
            return mark_safe(f'<a href="{obj.foto.url}" target="_blank"><img src="{obj.foto.url}" width="70" height="40" style="object-fit:cover; border-radius:6px; box-shadow:0 1px 3px rgba(0,0,0,0.2);" title="Klik untuk preview" /></a>')
        return "-"
    foto_preview.short_description = "Foto"

    def aksi(self, obj):
        from django.urls import reverse
        change_url = reverse('admin:landing_hero_change', args=[obj.id])
        delete_url = reverse('admin:landing_hero_delete', args=[obj.id])
        preview_url = obj.video_url or (obj.foto.url if obj.foto else '#')
        return mark_safe(f'<a href="{preview_url}" target="_blank" style="margin-right:8px; font-weight:600; color:#0f6b6b;">Preview</a><a href="{change_url}" style="margin-right:8px; font-weight:600; color:#d97706;">Edit</a><a href="{delete_url}" style="font-weight:600; color:#dc2626;">Hapus</a>')
    aksi.short_description = "Aksi"

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'post_date', 'views_count', 'total_likes_display', 'total_komentar_display')

    def total_likes_display(self, obj):
        return obj.total_likes
    total_likes_display.short_description = "Likes"

    def total_komentar_display(self, obj):
        return obj.total_komentar
    total_komentar_display.short_description = "Komentar"
    list_filter = ('post_date',)           # 'tanggal' diganti 'post_date'
    search_fields = ('judul', 'konten')
    ordering = ('-post_date',)             # 'tanggal' diganti 'post_date'

@admin.register(KomentarBerita)
class KomentarBeritaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'berita', 'email', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('nama', 'email', 'isi', 'berita__judul')
    list_editable = ('is_active',)


@admin.register(LikeBerita)
class LikeBeritaAdmin(admin.ModelAdmin):
    list_display = ('berita', 'session_key', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('berita__judul', 'session_key', 'ip_address')


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
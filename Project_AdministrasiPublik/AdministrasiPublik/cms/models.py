import os
import re
from io import BytesIO
from PIL import Image

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.base import ContentFile
from django_ckeditor_5.fields import CKEditor5Field


# ==========================================
# VALIDATOR & IMAGE RESIZE HELPERS
# ==========================================

def validate_favicon_file(value):
    max_size = 500 * 1024  # 500 KB
    if value.size > max_size:
        raise ValidationError("Ukuran file favicon tidak boleh melebihi 500 KB.")


def validate_logo_file(value):
    max_size = 2 * 1024 * 1024  # 2 MB
    if value.size > max_size:
        raise ValidationError("Ukuran file logo tidak boleh melebihi 2 MB.")


def resize_image_proportional(image_field, max_width=1200, max_height=600, quality=90):
    """
    Mengubah ukuran gambar secara proporsional jika melebihi batas resolusi
    tanpa merusak aspek rasio atau format transparansi.
    """
    if not image_field or not hasattr(image_field, 'file'):
        return

    try:
        img = Image.open(image_field)
        orig_width, orig_height = img.size

        # Cek jika gambar butuh di-resize
        if orig_width > max_width or orig_height > max_height:
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            output = BytesIO()
            img_format = img.format if img.format in ['PNG', 'JPEG', 'WEBP'] else 'PNG'
            
            if img_format == 'JPEG':
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                img.save(output, format='JPEG', quality=quality, optimize=True)
            else:
                img.save(output, format=img_format, optimize=True)
            
            output.seek(0)
            file_name = os.path.basename(image_field.name)
            image_field.save(file_name, ContentFile(output.read()), save=False)
    except Exception:
        # Jika bukan file gambar standar atau SVG, biarkan apa adanya
        pass


# ==========================================
# 1. MODEL HALAMAN DINAMIS (PAGE)
# ==========================================

CONTENT_TYPE_CHOICES = [
    ('html', 'HTML Content (CKEditor)'),
    ('pdf', 'PDF Preview (Embed Langsung)'),
    ('external_link', 'External Link (Redirect)'),
    ('internal_link', 'Internal Link (Route)'),
    ('dropdown', 'Dropdown Only (Induk Menu)'),
    ('file_download', 'File Download (Unduh Berkas)'),
]

PAGE_STATUS_CHOICES = [
    ('draft', 'Draft (Konsep)'),
    ('published', 'Published (Terbit)'),
]


class Page(models.Model):
    title = models.CharField(max_length=200, verbose_name="Judul Halaman")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug URL", help_text="Slug unik untuk URL halaman (contoh: kurikulum-2024, tentang-kami)")
    content_type = models.CharField(
        max_length=25, 
        choices=CONTENT_TYPE_CHOICES, 
        default='html', 
        verbose_name="Jenis Konten",
        help_text="Pilih jenis konten halaman ini"
    )
    
    # Konten HTML
    html_content = CKEditor5Field(blank=True, null=True, verbose_name="Isi Konten (HTML)", config_name='extends')
    
    # Berkas untuk PDF Preview & File Download
    file = models.FileField(
        upload_to='cms/pages/files/', 
        blank=True, 
        null=True, 
        verbose_name="File Berkas / PDF",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar'])],
        help_text="Upload berkas PDF untuk preview atau berkas unduhan"
    )
    
    # Tautan Eksternal & Internal
    external_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Tautan Eksternal", help_text="Contoh: https://siga-8.untad.ac.id")
    internal_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tautan Internal", help_text="Contoh: /berita/ atau /tenaga-pendidik/")
    
    # Status & SEO
    status = models.CharField(max_length=15, choices=PAGE_STATUS_CHOICES, default='published', verbose_name="Status Publikasi")
    meta_description = models.TextField(blank=True, null=True, verbose_name="Deskripsi Singkat / Ringkasan", help_text="Deskripsi singkat yang tampil pada header halaman")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui Pada")

    class Meta:
        verbose_name = "Halaman Dinamis"
        verbose_name_plural = "Daftar Halaman Dinamis"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()}) - [{self.status.upper()}]"

    def clean(self):
        super().clean()
        if self.content_type == 'external_link' and not self.external_url:
            raise ValidationError({'external_url': 'Tautan eksternal wajib diisi jika memilih jenis konten External Link.'})
        if self.content_type == 'internal_link' and not self.internal_url:
            raise ValidationError({'internal_url': 'Tautan internal wajib diisi jika memilih jenis konten Internal Link.'})
        if self.content_type in ['pdf', 'file_download'] and not self.file:
            raise ValidationError({'file': 'File berkas/PDF wajib diunggah untuk jenis konten PDF Preview atau File Download.'})

    def get_absolute_url(self):
        if self.content_type == 'external_link':
            return self.external_url or '#'
        elif self.content_type == 'internal_link':
            return self.internal_url or '#'
        elif self.content_type == 'file_download' and self.file:
            return self.file.url
        elif self.content_type == 'dropdown':
            return '#'
        return reverse('cms:page_detail', kwargs={'slug': self.slug})


# ==========================================
# 2. MODEL MENU & SUBMENU (DYNAMIC MENU)
# ==========================================

TARGET_CHOICES = [
    ('_self', 'Buka di Tab yang Sama (_self)'),
    ('_blank', 'Buka di Tab Baru (_blank)'),
]


class Menu(models.Model):
    title = models.CharField(max_length=150, verbose_name="Nama Menu")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name="Menu Induk (Parent)",
        help_text="Kosongkan jika ini adalah menu utama di navbar. Pilih induk jika ini adalah submenu/dropdown."
    )
    page = models.ForeignKey(
        Page, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='menus', 
        verbose_name="Halaman Terkait",
        help_text="Pilih halaman CMS yang terhubung dengan menu ini (jika ada)"
    )
    custom_url = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="URL Kustom",
        help_text="Isi jika menu mengarah ke URL eksternal / route internal tanpa halaman CMS (contoh: /berita/ atau /#sambutan)"
    )
    target = models.CharField(max_length=10, choices=TARGET_CHOICES, default='_self', verbose_name="Target Tautan")
    order = models.PositiveIntegerField(default=1, verbose_name="Nomor Urutan", help_text="Urutan posisi menu (angka lebih kecil tampil lebih awal)")
    is_active = models.BooleanField(default=True, verbose_name="Status Aktif", help_text="Centang untuk menampilkan menu di navbar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Menu Navigasi"
        verbose_name_plural = "Daftar Menu Navigasi"
        ordering = ['order', 'id']

    def __str__(self):
        if self.parent:
            return f"{self.parent.title} → {self.title}"
        return self.title

    def clean(self):
        super().clean()
        # Pencegahan Circular Parent Menu
        if self.parent:
            if self.pk and self.parent_id == self.pk:
                raise ValidationError({'parent': 'Menu tidak boleh menjadi induk bagi dirinya sendiri.'})
            ancestor = self.parent
            while ancestor:
                if self.pk and ancestor.pk == self.pk:
                    raise ValidationError({'parent': 'Terdeteksi relasi menu melingkar (circular parent).'})
                ancestor = ancestor.parent

    def get_url(self):
        """Menghasilkan URL tujuan menu secara cerdas"""
        if self.page:
            return self.page.get_absolute_url()
        if self.custom_url:
            return self.custom_url
        return '#'

    def get_target(self):
        """Menentukan apakah tautan dibuka di tab baru"""
        if self.page and self.page.content_type == 'external_link':
            return '_blank'
        return self.target

    @property
    def has_active_children(self):
        return self.children.filter(is_active=True).exists()

    def get_active_children(self):
        return self.children.filter(is_active=True).select_related('page', 'parent').order_by('order', 'id')


# ==========================================
# 3. MODEL SITE SETTINGS (SINGLE INSTANCE)
# ==========================================

SOCIAL_PLATFORM_CHOICES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('whatsapp', 'WhatsApp'),
    ('tiktok', 'TikTok'),
    ('youtube', 'YouTube'),
    ('x', 'X (Twitter)'),
    ('linkedin', 'LinkedIn'),
    ('telegram', 'Telegram'),
    ('threads', 'Threads'),
    ('pinterest', 'Pinterest'),
    ('snapchat', 'Snapchat'),
    ('discord', 'Discord'),
    ('reddit', 'Reddit'),
    ('line', 'LINE'),
    ('kaskus', 'Kaskus'),
    ('twitch', 'Twitch'),
]

SOCIAL_ICON_MAP = {
    'facebook': 'fa-brands fa-facebook-f',
    'instagram': 'fa-brands fa-instagram',
    'whatsapp': 'fa-brands fa-whatsapp',
    'tiktok': 'fa-brands fa-tiktok',
    'youtube': 'fa-brands fa-youtube',
    'x': 'fa-brands fa-x-twitter',
    'linkedin': 'fa-brands fa-linkedin-in',
    'telegram': 'fa-brands fa-telegram',
    'threads': 'fa-brands fa-threads',
    'pinterest': 'fa-brands fa-pinterest-p',
    'snapchat': 'fa-brands fa-snapchat',
    'discord': 'fa-brands fa-discord',
    'reddit': 'fa-brands fa-reddit-alien',
    'line': 'fa-brands fa-line',
    'kaskus': 'fa-solid fa-comments',
    'twitch': 'fa-brands fa-twitch',
}


class SiteSetting(models.Model):
    # Tab 1: Identitas Situs & Header
    favicon = models.ImageField(
        upload_to='site/favicons/', 
        blank=True, 
        null=True, 
        verbose_name="Favicon",
        validators=[FileExtensionValidator(allowed_extensions=['png', 'ico', 'svg']), validate_favicon_file],
        help_text="Format: .png / .ico / .svg, rasio 1:1, maksimal 500 KB"
    )
    header_logo = models.ImageField(
        upload_to='site/logos/', 
        blank=True, 
        null=True, 
        verbose_name="Logo Header",
        validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'svg', 'jpg', 'jpeg']), validate_logo_file],
        help_text="Format: .png / .webp / .svg (transparan), tinggi ideal ~80-120 px, maksimal 2 MB"
    )
    header_title = models.CharField(max_length=150, default="Administrasi Publik", verbose_name="Judul Header")
    header_subtitle = models.CharField(max_length=200, default="FISIP Universitas Tadulako", verbose_name="Subjudul Header")

    # Tab 2: Pengaturan Footer
    footer_logo = models.ImageField(
        upload_to='site/logos/', 
        blank=True, 
        null=True, 
        verbose_name="Logo Footer",
        validators=[FileExtensionValidator(allowed_extensions=['png', 'webp', 'svg', 'jpg', 'jpeg']), validate_logo_file],
        help_text="Format: .png / .webp / .svg (transparan), maksimal 2 MB"
    )
    footer_title = models.CharField(max_length=150, default="Administrasi Publik", verbose_name="Judul Footer")
    footer_subtitle = models.CharField(max_length=200, default="FISIP Universitas Tadulako", verbose_name="Subjudul Footer")
    footer_description = models.TextField(
        blank=True, 
        default="Program Studi Administrasi Publik Fakultas Ilmu Sosial dan Ilmu Politik Universitas Tadulako berorientasi pada integritas akademik, kualitas pendidikan, dan relevansi keprofesian.",
        verbose_name="Deskripsi Footer"
    )
    footer_short_address = models.CharField(max_length=255, default="Kampus Bumi Tadulako, Palu", verbose_name="Alamat Singkat Footer")

    # Tab 3: Kontak & Lokasi
    contact_title = models.CharField(max_length=150, default="Informasi Kontak", verbose_name="Judul Kontak")
    contact_subtitle = models.CharField(max_length=200, default="Program Studi Administrasi Publik", verbose_name="Subjudul Kontak")
    contact_address = models.TextField(
        default="Jl. Soekarno Hatta No.KM.9, Tondo, Kec. Mantikulore, Kota Palu, Sulawesi Tengah 94148", 
        verbose_name="Alamat Lengkap"
    )
    contact_phone = models.CharField(max_length=50, default="085330144401", verbose_name="Nomor Telepon")
    contact_whatsapp = models.CharField(
        max_length=50, 
        default="6285330144401", 
        verbose_name="Nomor WhatsApp",
        help_text="Gunakan format internasional 628xxx (tanpa tanda + atau spasi) agar otomatis terhubung ke wa.me"
    )
    contact_email = models.EmailField(default="Admpublik.FISIP@untad.ac.id", verbose_name="Email Kontak")
    maps_embed_url = models.TextField(
        blank=True, 
        null=True, 
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3989.3082596245!2d119.8912!3d-0.8587!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zCsKuwqDCtsKqwqDCtsKqwqA!5e0!3m2!1sid!2sid!4v1600000000000!5m2!1sid!2sid", 
        verbose_name="URL Embed Iframe Google Maps"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengaturan Situs (Site Setting)"
        verbose_name_plural = "Pengaturan Situs (Site Settings)"

    def __str__(self):
        return f"Pengaturan Situs: {self.header_title}"

    @classmethod
    def get_solo(cls):
        """Memastikan selalu ada satu instance SiteSetting yang aktif (Single Instance pattern)"""
        obj, created = cls.objects.get_or_create(id=1)
        return obj

    def clean(self):
        super().clean()
        if self.contact_whatsapp:
            # Standarisasi format WhatsApp ke 628xxx
            digits = re.sub(r'\D', '', self.contact_whatsapp)
            if digits.startswith('08'):
                digits = '628' + digits[2:]
            elif digits.startswith('8'):
                digits = '628' + digits[1:]
            self.contact_whatsapp = digits

    def save(self, *args, **kwargs):
        # Auto-resize gambar untuk optimasi performa loading
        if self.favicon:
            resize_image_proportional(self.favicon, max_width=256, max_height=256)
        if self.header_logo:
            resize_image_proportional(self.header_logo, max_width=1200, max_height=400)
        if self.footer_logo:
            resize_image_proportional(self.footer_logo, max_width=1200, max_height=400)
        
        # Selalu paksa id=1 agar menjadi Single Instance
        self.id = 1
        super().save(*args, **kwargs)

    @property
    def get_whatsapp_clean(self):
        digits = re.sub(r'\D', '', self.contact_whatsapp or '')
        if digits.startswith('08'):
            digits = '628' + digits[2:]
        return digits or '6285330144401'


# ==========================================
# 4. MODEL MEDIA SOSIAL (ITEM DINAMIS)
# ==========================================

class SocialMedia(models.Model):
    setting = models.ForeignKey(SiteSetting, on_delete=models.CASCADE, related_name='social_media_list', verbose_name="Pengaturan Situs")
    platform = models.CharField(max_length=30, choices=SOCIAL_PLATFORM_CHOICES, verbose_name="Platform Sosial Media")
    url = models.URLField(max_length=500, verbose_name="URL Profil / Tautan", help_text="Contoh: https://instagram.com/admpublik_untad")
    order = models.PositiveIntegerField(default=1, verbose_name="Nomor Urut")
    is_active = models.BooleanField(default=True, verbose_name="Status Aktif", help_text="Centang untuk menampilkan di website")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sosial Media"
        verbose_name_plural = "Daftar Sosial Media"
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"

    @property
    def icon_class(self):
        return SOCIAL_ICON_MAP.get(self.platform, 'fa-solid fa-share-nodes')


# ==========================================
# 5. MODEL TAUTAN CEPAT (ITEM DINAMIS)
# ==========================================

class QuickLink(models.Model):
    setting = models.ForeignKey(SiteSetting, on_delete=models.CASCADE, related_name='quick_links', verbose_name="Pengaturan Situs")
    title = models.CharField(max_length=150, verbose_name="Judul Tautan", help_text="Contoh: Website UNTAD, SIGA-8, Sertifikat Akreditasi")
    url = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Tautan URL", 
        help_text="Bisa link eksternal (https://...) atau internal (/...)"
    )
    file = models.FileField(
        upload_to='site/quick_links/', 
        blank=True, 
        null=True, 
        verbose_name="Upload File Berkas / Dokumen (Opsional)",
        help_text="Upload jika tautan berupa file (misal: PDF Sertifikat Akreditasi)"
    )
    open_in_new_tab = models.BooleanField(default=False, verbose_name="Buka di Tab Baru")
    order = models.PositiveIntegerField(default=1, verbose_name="Nomor Urut")
    is_active = models.BooleanField(default=True, verbose_name="Status Aktif")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tautan Cepat (Footer)"
        verbose_name_plural = "Daftar Tautan Cepat (Footer)"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def get_url(self):
        if self.file:
            return self.file.url
        return self.url or '#'

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field  # type: ignore


class Page(models.Model):
    """
    Model representasi Halaman Dinamis dalam CMS.
    Mendukung berbagai tipe konten: HTML, PDF Preview, External Link, Internal Link, File Download, dan Dropdown Only.
    """
    CONTENT_TYPE_CHOICES = [
        ('html', 'HTML Content (CKEditor 5)'),
        ('pdf', 'PDF Preview (Dokumen Terbuka di Layar)'),
        ('external_link', 'External Link (Tautan Eksternal / Redirect)'),
        ('internal_link', 'Internal Link (Halaman Internal Sistem)'),
        ('file_download', 'File Download (Langsung Mengunduh Berkas)'),
        ('dropdown_only', 'Dropdown Only (Induk Submenu Tanpa Halaman)'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft (Belum Dipublikasikan)'),
        ('published', 'Published (Diterbitkan & Aktif)'),
    ]

    title = models.CharField(
        max_length=200, 
        verbose_name="Judul Halaman"
    )
    slug = models.SlugField(
        max_length=200, 
        unique=True, 
        verbose_name="Slug URL",
        help_text="Pengenal unik untuk rute halaman di URL (contoh: panduan-akademik, profil-lulusan)"
    )
    content_type = models.CharField(
        max_length=20, 
        choices=CONTENT_TYPE_CHOICES, 
        default='html', 
        verbose_name="Jenis Konten"
    )
    
    # Konten HTML menggunakan CKEditor 5
    html_content = CKEditor5Field(
        'Konten HTML Halaman', 
        config_name='extends', 
        blank=True, 
        null=True
    )
    
    # Dokumen PDF untuk preview langsung
    pdf_file = models.FileField(
        upload_to='cms/pdf/', 
        blank=True, 
        null=True, 
        verbose_name="File Dokumen PDF",
        help_text="Format .pdf untuk dipratinjau langsung di halaman website"
    )
    
    # Berkas unduhan langsung
    file_download = models.FileField(
        upload_to='cms/downloads/', 
        blank=True, 
        null=True, 
        verbose_name="Berkas Unduhan",
        help_text="Berkas yang dapat langsung diunduh pengunjung saat tautan diklik"
    )
    
    # Tautan Eksternal & Internal
    external_url = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="URL Eksternal",
        help_text="Contoh: https://siga-8.untad.ac.id (harus diawali http:// atau https://)"
    )
    internal_url = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="URL Internal",
        help_text="Contoh: /berita/ atau /event/ (harus diawali garis miring /)"
    )

    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='published', 
        verbose_name="Status Publikasi"
    )
    meta_description = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Subjudul / Deskripsi Singkat",
        help_text="Deskripsi singkat yang tampil di bawah judul halaman"
    )
    banner_image = models.ImageField(
        upload_to='cms/banners/', 
        blank=True, 
        null=True, 
        verbose_name="Gambar Banner / Sampul (Opsional)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Halaman CMS"
        verbose_name_plural = "Daftar Halaman CMS"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()}) [{self.get_status_display()}]"

    def clean(self):
        super().clean()
        
        # 1. Validasi reserved slugs
        reserved_slugs = ['admin', 'dashboard', 'login', 'logout', 'register', 'api', 'media', 'static', 'page']
        if self.slug and self.slug.strip().lower() in reserved_slugs:
            raise ValidationError({'slug': f"Slug '{self.slug}' tidak boleh digunakan karena merupakan rute bawaan sistem."})

        # 2. Validasi per Content Type
        if self.content_type == 'html':
            if self.status == 'published' and not (self.html_content and self.html_content.strip()):
                raise ValidationError({'html_content': 'Konten HTML wajib diisi jika status halaman adalah Published.'})
        elif self.content_type == 'pdf':
            if not self.pdf_file:
                raise ValidationError({'pdf_file': 'File PDF wajib diunggah jika memilih jenis konten PDF Preview.'})
            if self.pdf_file and not self.pdf_file.name.lower().endswith('.pdf'):
                raise ValidationError({'pdf_file': 'File yang diunggah harus berformat PDF (.pdf).'})
        elif self.content_type == 'external_link':
            if not self.external_url:
                raise ValidationError({'external_url': 'URL Eksternal wajib diisi jika memilih jenis konten External Link.'})
            if not (self.external_url.startswith('http://') or self.external_url.startswith('https://')):
                raise ValidationError({'external_url': 'URL Eksternal harus diawali dengan http:// atau https://'})
        elif self.content_type == 'internal_link':
            if not self.internal_url:
                raise ValidationError({'internal_url': 'URL Internal wajib diisi jika memilih jenis konten Internal Link.'})
            if not self.internal_url.startswith('/'):
                raise ValidationError({'internal_url': 'URL Internal harus diawali dengan garis miring (/), contoh: /berita/'})
        elif self.content_type == 'file_download':
            if not self.file_download:
                raise ValidationError({'file_download': 'Berkas unduhan wajib diunggah jika memilih jenis konten File Download.'})

    def get_absolute_url(self):
        return reverse('cms_page_detail', kwargs={'slug': self.slug})


class Menu(models.Model):
    """
    Model representasi Elemen Menu Navigasi (Navbar).
    Mendukung hirarki bertingkat (Parent & Multilevel Submenu), status aktif,
    urutan tampilan (ordering), dan keterhubungan dengan Halaman CMS.
    """
    TARGET_CHOICES = [
        ('_self', 'Tab yang Sama (_self)'),
        ('_blank', 'Tab Baru (_blank)'),
    ]

    title = models.CharField(
        max_length=100, 
        verbose_name="Nama / Label Menu",
        help_text="Teks yang tampil pada navbar"
    )
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children', 
        verbose_name="Induk Menu (Parent)",
        help_text="Pilih menu induk jika ini merupakan submenu/dropdown. Kosongkan jika menu utama baris teratas."
    )
    page = models.ForeignKey(
        Page, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='menus', 
        verbose_name="Halaman Terkait (CMS Page)",
        help_text="Pilih halaman CMS yang dituju saat menu ini diklik"
    )
    url_override = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Custom URL (Opsional)",
        help_text="Jika diisi, menu akan diarahkan ke URL ini secara langsung mengabaikan Halaman Terkait"
    )
    target = models.CharField(
        max_length=10, 
        choices=TARGET_CHOICES, 
        default='_self', 
        verbose_name="Target Tautan"
    )
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="Urutan Tampilan",
        help_text="Urutan posisi (angka lebih kecil berada di kiri / atas)"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Status Aktif",
        help_text="Centang untuk menampilkan menu pada navbar website"
    )
    icon_class = models.CharField(
        max_length=60, 
        blank=True, 
        null=True, 
        default="", 
        verbose_name="Icon FontAwesome (Opsional)",
        help_text="Contoh: fas fa-landmark, fas fa-bullseye, fas fa-book"
    )

    class Meta:
        verbose_name = "Menu Navigasi"
        verbose_name_plural = "Daftar Menu Navigasi"
        ordering = ['order', 'id']

    def __str__(self):
        if self.parent:
            return f"└─ {self.title} (Submenu dari: {self.parent.title})"
        return f"{self.title} (Menu Utama)"

    def clean(self):
        super().clean()
        
        # 1. Pencegahan circular parent reference
        if self.parent:
            if self.pk and self.parent_id == self.pk:
                raise ValidationError({'parent': 'Menu tidak dapat menjadikan dirinya sendiri sebagai menu induk.'})
            
            # Telusuri rantai induk ke atas
            curr = self.parent
            visited = {self.pk} if self.pk else set()
            while curr:
                if curr.pk in visited:
                    raise ValidationError({'parent': f"Terdeteksi loop sirkular pada menu '{curr.title}'. Menu tidak dapat menjadi turunan dari anaknya sendiri."})
                visited.add(curr.pk)
                curr = curr.parent

        # 2. Validasi URL Override
        if self.url_override and self.url_override.strip():
            url = self.url_override.strip()
            if not (url.startswith('http://') or url.startswith('https://') or url.startswith('/') or url.startswith('#')):
                raise ValidationError({'url_override': 'Custom URL harus diawali dengan http://, https://, /, atau #'})

    @property
    def has_children(self):
        """Mengecek apakah menu ini memiliki submenu aktif."""
        return self.children.filter(is_active=True).exists()

    @property
    def active_children(self):
        """Mengambil submenu aktif yang terurut."""
        return self.children.filter(is_active=True).order_by('order', 'id')

    def get_url(self):
        """
        Menentukan URL target secara dinamis berdasarkan prioritas:
        1. Custom URL Override (jika diisi)
        2. Halaman CMS (berdasarkan content_type halaman)
        3. '#' jika bertindak sebagai dropdown parent saja.
        """
        if self.url_override and self.url_override.strip():
            return self.url_override.strip()
            
        if self.page:
            p = self.page
            if p.content_type == 'external_link' and p.external_url:
                return p.external_url
            elif p.content_type == 'internal_link' and p.internal_url:
                return p.internal_url
            elif p.content_type == 'file_download' and p.file_download:
                return p.file_download.url
            elif p.content_type == 'dropdown_only':
                return '#'
            else:
                return reverse('cms_page_detail', kwargs={'slug': p.slug})
                
        return '#'

    def get_target(self):
        """Menentukan target tab (_self atau _blank)."""
        if self.target == '_blank':
            return '_blank'
        if self.page and self.page.content_type == 'external_link':
            return '_blank'
        return self.target or '_self'

import io
import os
import re
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field  # type: ignore
from .validators import (
    validate_image_file,
    validate_video_file,
    validate_pdf_file,
    validate_document_file,
    validate_favicon_file,
    validate_site_logo_file,
)


# 1. Model Sambutan Koordinator Prodi (Menggunakan CKEditor 5)
class Sambutan(models.Model):
    judul = models.CharField(max_length=200, default="Sambutan Koordinator Prodi")
    isi = CKEditor5Field('Isi Sambutan', config_name='extends')
    nama_author = models.CharField(max_length=150, verbose_name="Nama Pimpinan / Koordinator")
    foto = models.ImageField(
        upload_to='sambutan/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Upload foto resmi koordinator prodi (JPG, PNG, WEBP maks 10 MB)"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Sambutan Koordinator Prodi"
        verbose_name_plural = "Sambutan Koordinator Prodi"

    def __str__(self):
        return f"{self.judul} - {self.nama_author}"


# 2. Model Galeri Kegiatan
class Galeri(models.Model):
    judul = models.CharField(max_length=200, blank=True, default="Dokumentasi Kegiatan", help_text="Keterangan / Judul foto kegiatan")
    gambar = models.ImageField(
        upload_to='galeri/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Upload foto dokumentasi kegiatan (JPG, PNG, WEBP maks 10 MB)"
    )
    urutan = models.PositiveIntegerField(default=1, help_text="Urutan posisi foto di galeri beranda (contoh: 1, 2, 3...)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Galeri Kegiatan"
        verbose_name_plural = "Galeri Kegiatan"
        ordering = ['urutan', '-created_at']

    def __str__(self):
        return f"[{self.urutan}] {self.judul or 'Foto Galeri'}"


# 2.1 Model Hero Beranda (Video & Foto Background)
class Hero(models.Model):
    judul = models.CharField(max_length=255, blank=True, default="Program Studi Administrasi Publik", help_text="Judul utama hero")
    subjudul = models.CharField(max_length=255, blank=True, default="Welcome to", help_text="Subjudul kecil di atas judul utama")
    deskripsi = models.TextField(blank=True, default="Fakultas Ilmu Sosial dan Ilmu Politik\nUniversitas Tadulako", help_text="Deskripsi singkat hero")
    link_video = models.CharField(max_length=500, blank=True, null=True, help_text="Link video YouTube atau URL file MP4")
    video_file = models.FileField(
        upload_to='hero/video/',
        blank=True,
        null=True,
        validators=[validate_video_file],
        help_text="Upload file video (MP4/WEBM/OGG, maksimal 100 MB)"
    )
    foto = models.ImageField(
        upload_to='hero/foto/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Upload Gambar Hero (JPG, PNG, WEBP maks 10 MB)"
    )
    is_active = models.BooleanField(default=True, help_text="Aktifkan sebagai tampilan hero utama di Beranda")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hero Beranda"
        verbose_name_plural = "Manajemen Hero"
        ordering = ['-is_active', '-created_at']

    def __str__(self):
        return self.judul or f"Hero #{self.id}"

    @property
    def youtube_embed_url(self):
        """Mengonversi link YouTube (watch, youtu.be, shorts, embed, live) ke URL embed autoplay background"""
        if not self.link_video:
            return ""
        url = self.link_video.strip()
        lower_url = url.lower()
        if not any(domain in lower_url for domain in ('youtube.com', 'youtu.be', 'youtube-nocookie.com')):
            return ""
        import re
        match = re.search(
            r'(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/|v\/))([0-9A-Za-z_-]{11})',
            url
        )
        if match:
            video_id = match.group(1)
            return (
                f"https://www.youtube.com/embed/{video_id}"
                f"?autoplay=1&mute=1&loop=1&playlist={video_id}&controls=0&rel=0&playsinline=1&iv_load_policy=3"
            )
        return ""


# 3. Model Berita (Dilengkapi Views & Likes)
class Berita(models.Model):
    judul = models.CharField(max_length=255)
    ringkasan = models.TextField(blank=True, null=True)
    konten = CKEditor5Field('Konten Berita', config_name='extends')
    gambar = models.ImageField(
        upload_to='berita/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Upload foto/gambar berita (JPG, PNG, WEBP maks 10 MB)"
    )
    views = models.PositiveIntegerField(default=0, verbose_name="Jumlah Dilihat")
    likes = models.PositiveIntegerField(default=0, verbose_name="Jumlah Suka")
    shares = models.PositiveIntegerField(default=0, verbose_name="Jumlah Dibagikan")
    posted_at = models.DateTimeField(default=timezone.now, verbose_name="Waktu Tayang / Post")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Waktu Diperbarui")

    class Meta:
        verbose_name = "Berita"
        verbose_name_plural = "Daftar Berita"
        ordering = ['-posted_at']

    def __str__(self):
        return self.judul


# 3.1 Model Komentar Berita Pengunjung
class KomentarBerita(models.Model):
    berita = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='komentar_list', verbose_name="Berita")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='komentar_list', verbose_name="Pengguna")
    nama = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    email = models.EmailField(blank=True, null=True, verbose_name="Email (Opsional)")
    isi = models.TextField(verbose_name="Isi Komentar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Dikirim")

    class Meta:
        verbose_name = "Komentar Berita"
        verbose_name_plural = "Daftar Komentar Berita"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nama} pada {self.berita.judul}"


# 4. Tabel Khusus Pangkat & Golongan (PNS & PPPK)
class PangkatGolongan(models.Model):
    KATEGORI_CHOICES = (
        ('PNS', 'PNS'),
        ('PPPK', 'PPPK'),
    )
    nama = models.CharField(max_length=150, help_text="Contoh: Penata Muda - III/a atau Golongan IX (Ahli Pertama)")
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES, default='PNS')

    class Meta:
        verbose_name = "Pangkat Golongan"
        verbose_name_plural = "Daftar Pangkat Golongan"
        ordering = ['kategori', 'id']

    def __str__(self):
        return f"{self.nama} ({self.kategori})"


# 5. Model Tenaga Pendidik & Kependidikan
class TenagaPendidik(models.Model):
    JENIS_CHOICES = [
        ('DOSEN', 'Dosen Pengajar'),
        ('TENDIK', 'Tenaga Kependidikan'),
    ]

    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    STATUS_CHOICES = [
        ('DOSEN TETAP', 'DOSEN TETAP'),
        ('DOSEN LUAR BIASA', 'DOSEN LUAR BIASA'),
        ('PROFESOR', 'PROFESOR'),
        ('STAF ADMINISTRASI', 'STAF ADMINISTRASI'),
        ('KEPALA TATA USAHA', 'KEPALA TATA USAHA'),
    ]

    JABATAN_FUNGSIONAL_CHOICES = [
        ('Guru Besar', 'Guru Besar'),
        ('Lektor Kepala', 'Lektor Kepala'),
        ('Lektor', 'Lektor'),
        ('Asisten Ahli', 'Asisten Ahli'),
        ('Tenaga Pengajar', 'Tenaga Pengajar'),
    ]

    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='DOSEN')
    nama = models.CharField(max_length=200, help_text="Nama lengkap beserta gelar")
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, default='L', verbose_name="Jenis Kelamin")
    jabatan_fungsional = models.CharField(
        max_length=50,
        choices=JABATAN_FUNGSIONAL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Jabatan Fungsional",
        help_text="Pilihan jabatan fungsional dosen (cth: Guru Besar, Lektor Kepala, Lektor, Asisten Ahli)"
    )
    bidang_ilmu = models.CharField(max_length=200, verbose_name="Bidang Ilmu / Jabatan")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DOSEN TETAP')
    foto = models.ImageField(
        upload_to='pegawai/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Upload foto rasio 1:1 (JPG, PNG, WEBP maks 10 MB)"
    )

    # Identitas Kepegawaian (blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIDN")
    nip = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIP")
    nuptk = models.CharField(max_length=50, blank=True, null=True, verbose_name="NUPTK")
    no_hp = models.CharField(max_length=30, blank=True, null=True, verbose_name="No. HP / WhatsApp")

    pangkat_golongan = models.ForeignKey(
        PangkatGolongan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pegawai_list',
        verbose_name="Pangkat / Golongan"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tenaga Pendidik & Kependidikan"
        verbose_name_plural = "Tenaga Pendidik & Kependidikan"
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.jenis})"

    @property
    def jabatan(self):
        return self.jabatan_fungsional or self.status or "Dosen Tetap"

    @property
    def bidang_keahlian(self):
        return self.bidang_ilmu or "Ilmu Administrasi Publik"


# 6. Model Audit Log
class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp.strftime('%d/%m/%Y %H:%M')}] {self.action} oleh {self.user}"


# 7. Model Halaman Tentang (LENGKAP: Profil, Sejarah, Struktur, Profil Lulusan, Akreditasi)
class HalamanTentang(models.Model):
    KATEGORI_CHOICES = [
        ('profil', 'Profil Program Studi'),
        ('sejarah', 'Sejarah Singkat'),
        ('struktur', 'Struktur Organisasi'),
        ('profil_lulusan', 'Profil Lulusan'),
        ('akreditasi', 'Sertifikat Akreditasi'),
    ]
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, unique=True)
    judul = models.CharField(max_length=255)
    gambar = models.ImageField(
        upload_to='tentang/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Bagan / Gambar",
        help_text="Upload gambar/bagan (JPG, PNG, atau WEBP maks 10 MB)"
    )
    file_utama = models.FileField(
        upload_to='tentang/berkas/',
        blank=True,
        null=True,
        validators=[validate_pdf_file],
        verbose_name="Berkas / Dokumen PDF",
        help_text="Upload dokumen PDF resmi (maks 20 MB)"
    )
    isi = CKEditor5Field('Isi Konten / Keterangan', config_name='extends', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Halaman Tentang"
        verbose_name_plural = "Daftar Halaman Tentang"

    def __str__(self):
        return self.get_kategori_display()


# 8. Model Visi, Misi, dan Tujuan (Terstruktur)
class VisiMisiTujuan(models.Model):
    visi_teks = models.TextField(
        verbose_name="Teks Visi",
        default="Menjadi program studi yang unggul secara global dalam bidang ilmu administrasi publik sebagai mitra strategis untuk kehidupan yang lebih baik bagi Rakyat Indonesia dan Umat Manusia melalui pendidikan, penelitian, dan pelayanan tata kelola publik yang berwawasan lingkungan dan berkelanjutan."
    )
    misi_intro = models.CharField(
        max_length=255,
        default="Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki misi sebagai berikut:",
        verbose_name="Kalimat Pengantar Misi"
    )
    tujuan_intro = models.CharField(
        max_length=255,
        default="Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki tujuan Pendidikan berupa:",
        verbose_name="Kalimat Pengantar Tujuan"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Visi, Misi & Tujuan"
        verbose_name_plural = "Visi, Misi & Tujuan"

    def __str__(self):
        return "Pengaturan Visi, Misi & Tujuan"


class MisiItem(models.Model):
    visi_misi = models.ForeignKey(
        VisiMisiTujuan,
        on_delete=models.CASCADE,
        related_name='misi_items',
        null=True,
        blank=True
    )
    urutan = models.PositiveIntegerField(default=1, verbose_name="Nomor Urut")
    isi = models.TextField(verbose_name="Isi Poin Misi")

    class Meta:
        verbose_name = "Poin Misi"
        verbose_name_plural = "Daftar Poin Misi"
        ordering = ['urutan', 'id']

    def __str__(self):
        return f"{self.urutan}. {self.isi[:60]}..."


class TujuanItem(models.Model):
    visi_misi = models.ForeignKey(
        VisiMisiTujuan,
        on_delete=models.CASCADE,
        related_name='tujuan_items',
        null=True,
        blank=True
    )
    urutan = models.PositiveIntegerField(default=1, verbose_name="Nomor Urut")
    judul = models.CharField(
        max_length=200,
        verbose_name="Judul Tujuan",
        help_text="Contoh: Employabilitas"
    )
    subjudul = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Subjudul (English / Keterangan)",
        help_text="Contoh: Employability"
    )
    deskripsi = models.TextField(verbose_name="Deskripsi Tujuan")

    class Meta:
        verbose_name = "Poin Tujuan"
        verbose_name_plural = "Daftar Poin Tujuan"
        ordering = ['urutan', 'id']

    def __str__(self):
        return f"{self.urutan}. {self.judul}"


# 9. Model Halaman Akademik (SIGA-8, Kurikulum, Jadwal, RPS, Panduan)
class HalamanAkademik(models.Model):
    KATEGORI_CHOICES = [
        ('siga8', 'SIGA-8'),
        ('kurikulum', 'Kurikulum'),
        ('jadwal', 'Jadwal Perkuliahan'),
        ('rps', 'RPS'),
        ('panduan', 'Panduan Akademik'),
    ]
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, unique=True, verbose_name="Kategori Menu")
    judul = models.CharField(max_length=255, verbose_name="Judul Halaman")
    subjudul = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subjudul / Ringkasan")
    isi = CKEditor5Field('Isi Konten Akademik', config_name='extends', blank=True, null=True)
    link_eksternal = models.URLField(blank=True, null=True, verbose_name="Tautan Eksternal / Portal")
    file_utama = models.FileField(
        upload_to='akademik/dokumen/',
        blank=True,
        null=True,
        validators=[validate_document_file],
        verbose_name="Dokumen Utama (PDF/Word/Excel/PPT)"
    )
    nama_file_utama = models.CharField(max_length=150, blank=True, null=True, verbose_name="Label Tombol Unduh", help_text="Contoh: Unduh Kurikulum Lengkap (PDF)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Halaman Akademik"
        verbose_name_plural = "Daftar Halaman Akademik"
        ordering = ['id']

    def __str__(self):
        return self.get_kategori_display()

    def get_kondisi_tampilan(self):
        """
        Menentukan kondisi tampilan berdasarkan input admin:
        - Kondisi A: Hanya link_eksternal yang diisi (isi & file_utama kosong) -> Redirect langsung
        - Kondisi B: Hanya file_utama yang diunggah (link_eksternal & isi kosong) -> Preview PDF langsung
        - Kondisi C: Ada isi konten teks (dan/atau lampiran file) -> Halaman detail konten + download/preview
        """
        import re
        isi_clean = re.sub(r'<[^>]*>', '', self.isi or '').replace('&nbsp;', '').strip()
        has_isi = bool(isi_clean)
        has_file = bool(self.file_utama)
        has_link = bool(self.link_eksternal and self.link_eksternal.strip())

        # Kondisi A: Hanya link eksternal yang diisi
        if has_link and not has_isi and not has_file:
            return 'A'
        # Kondisi B: Hanya file dokumen/PDF yang diunggah
        elif has_file and not has_isi and not has_link:
            return 'B'
        # Kondisi C: Ada konten teks (dan/atau ada file)
        else:
            return 'C'


# 10. Model Berkas / Lampiran Tambahan untuk Halaman Akademik
class DokumenAkademik(models.Model):
    halaman = models.ForeignKey(HalamanAkademik, on_delete=models.CASCADE, related_name='dokumen_list', verbose_name="Halaman Terkait")
    judul = models.CharField(max_length=255, verbose_name="Nama Dokumen / Berkas")
    file = models.FileField(
        upload_to='akademik/berkas/',
        validators=[validate_document_file],
        verbose_name="Upload File (PDF/Doc/Xls/Ppt)"
    )
    keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan Singkat")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Unggah")

    class Meta:
        verbose_name = "Dokumen / Berkas Akademik"
        verbose_name_plural = "Daftar Dokumen Akademik"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.judul} ({self.halaman.get_kategori_display()})"


# 11. Model Statistik Pengunjung Otomatis
class Pengunjung(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Alamat IP")
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name="Kunci Sesi")
    user_agent = models.CharField(max_length=255, blank=True, null=True, verbose_name="User Agent")
    path = models.CharField(max_length=255, blank=True, null=True, verbose_name="Halaman Terakhir")
    tanggal = models.DateField(default=timezone.localdate, db_index=True, verbose_name="Tanggal Kunjungan")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Kunjungan")

    class Meta:
        verbose_name = "Data Pengunjung"
        verbose_name_plural = "Statistik Pengunjung"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tanggal']),
            models.Index(fields=['ip_address', 'tanggal']),
        ]

    def __str__(self):
        return f"{self.ip_address or 'Anonim'} - {self.tanggal} ({self.created_at.strftime('%H:%M')})"


class PengunjungTotal(models.Model):
    total_awal = models.PositiveIntegerField(default=6320, verbose_name="Angka Dasar Total Pengunjung", help_text="Offset bawaan untuk total statistik")
    hari_ini_awal = models.PositiveIntegerField(default=24, verbose_name="Angka Dasar Pengunjung Hari Ini", help_text="Offset bawaan untuk hari pertama")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pengaturan Statistik Pengunjung"
        verbose_name_plural = "Pengaturan Statistik Pengunjung"

    def __str__(self):
        return f"Konfigurasi Statistik (Awal: {self.total_awal})"


# ==========================================
# 12. MODEL EVENT / AGENDA TERDEKAT (Rasio Poster 4:5)
# ==========================================
class Event(models.Model):
    KATEGORI_CHOICES = [
        ('Seminar', 'Seminar'),
        ('Kuliah Tamu', 'Kuliah Tamu'),
        ('Agenda Prodi', 'Agenda Prodi'),
        ('Workshop', 'Workshop / Pelatihan'),
        ('Lomba', 'Lomba / Kompetisi'),
        ('Lainnya', 'Lainnya'),
    ]

    judul = models.CharField(max_length=255, verbose_name="Judul Event")
    slug = models.SlugField(max_length=255, unique=True, blank=True, help_text="Otomatis digenerate dari judul acara")
    poster = models.ImageField(
        upload_to='event_posters/',
        blank=True,
        null=True,
        validators=[validate_image_file],
        help_text="Gunakan gambar poster dengan rasio 4:5 (contoh: 1080x1350 px)"
    )
    tanggal_mulai = models.DateField(verbose_name="Tanggal Mulai")
    tanggal_selesai = models.DateField(blank=True, null=True, verbose_name="Tanggal Selesai (Opsional)")
    waktu = models.CharField(max_length=100, default="08.00 WITA - Selesai", verbose_name="Waktu Pelaksanaan", help_text="Contoh: 08.00 WITA - Selesai")
    lokasi = models.CharField(max_length=255, verbose_name="Lokasi / Tempat", help_text="Contoh: Gedung Teater FISIP UNTAD / Zoom Cloud Meetings")
    kategori = models.CharField(max_length=100, choices=KATEGORI_CHOICES, default='Seminar', verbose_name="Kategori Event")
    deskripsi = CKEditor5Field('Deskripsi Lengkap Event', config_name='extends', blank=True, null=True)
    link_pendaftaran = models.URLField(max_length=500, blank=True, null=True, verbose_name="Link Pendaftaran (Opsional)", help_text="Contoh: https://bit.ly/daftar-acara-ap")
    is_active = models.BooleanField(default=True, verbose_name="Aktif / Tampilkan di Beranda")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")

    class Meta:
        verbose_name = "Event & Agenda"
        verbose_name_plural = "Daftar Event & Agenda"
        ordering = ['tanggal_mulai', '-created_at']

    def __str__(self):
        return f"{self.judul} ({self.tanggal_mulai})"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.judul) or "event"
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def hari_mulai(self):
        return self.tanggal_mulai.strftime("%d") if self.tanggal_mulai else ""

    @property
    def bulan_mulai_singkat(self):
        if not self.tanggal_mulai:
            return ""
        BULAN_SINGKAT = {
            1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MEI", 6: "JUN",
            7: "JUL", 8: "AGU", 9: "SEP", 10: "OKT", 11: "NOV", 12: "DES"
        }
        return BULAN_SINGKAT.get(self.tanggal_mulai.month, self.tanggal_mulai.strftime("%b").upper())

    @property
    def tanggal_display(self):
        if not self.tanggal_mulai:
            return ""
        BULAN_NAMA = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
            7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }
        tgl_mulai_str = f"{self.tanggal_mulai.day} {BULAN_NAMA.get(self.tanggal_mulai.month, '')} {self.tanggal_mulai.year}"
        if self.tanggal_selesai and self.tanggal_selesai != self.tanggal_mulai:
            if self.tanggal_mulai.month == self.tanggal_selesai.month and self.tanggal_mulai.year == self.tanggal_selesai.year:
                return f"{self.tanggal_mulai.day} - {self.tanggal_selesai.day} {BULAN_NAMA.get(self.tanggal_selesai.month, '')} {self.tanggal_selesai.year}"
            return f"{tgl_mulai_str} s/d {self.tanggal_selesai.day} {BULAN_NAMA.get(self.tanggal_selesai.month, '')} {self.tanggal_selesai.year}"
        return tgl_mulai_str

    @property
    def tanggal_timeline(self):
        if not self.tanggal_mulai:
            return ""
        HARI_NAMA = {
            0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 4: "Jumat", 5: "Sabtu", 6: "Minggu"
        }
        BULAN_NAMA = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
            7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }
        hari = HARI_NAMA.get(self.tanggal_mulai.weekday(), "")
        bulan = BULAN_NAMA.get(self.tanggal_mulai.month, "")
        return f"{hari} {self.tanggal_mulai.day} {bulan} {self.tanggal_mulai.year}"


# =========================================================================
# MODEL KONFIGURASI SITUS TERPADU (SITE SETTINGS)
# =========================================================================

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

PLATFORM_ICONS = {
    'facebook': 'bi bi-facebook',
    'instagram': 'bi bi-instagram',
    'whatsapp': 'bi bi-whatsapp',
    'tiktok': 'bi bi-tiktok',
    'youtube': 'bi bi-youtube',
    'x': 'bi bi-twitter-x',
    'linkedin': 'bi bi-linkedin',
    'telegram': 'bi bi-telegram',
    'threads': 'bi bi-threads',
    'pinterest': 'bi bi-pinterest',
    'snapchat': 'bi bi-snapchat',
    'discord': 'bi bi-discord',
    'reddit': 'bi bi-reddit',
    'line': 'bi bi-line',
    'kaskus': 'bi bi-chat-quote-fill',
    'twitch': 'bi bi-twitch',
}

PLATFORM_FA_ICONS = {
    'facebook': 'fab fa-facebook-f',
    'instagram': 'fab fa-instagram',
    'whatsapp': 'fab fa-whatsapp',
    'tiktok': 'fab fa-tiktok',
    'youtube': 'fab fa-youtube',
    'x': 'fab fa-x-twitter',
    'linkedin': 'fab fa-linkedin-in',
    'telegram': 'fab fa-telegram-plane',
    'threads': 'fab fa-threads',
    'pinterest': 'fab fa-pinterest',
    'snapchat': 'fab fa-snapchat',
    'discord': 'fab fa-discord',
    'reddit': 'fab fa-reddit',
    'line': 'fab fa-line',
    'kaskus': 'fas fa-comments',
    'twitch': 'fab fa-twitch',
}


def _resize_site_image(image_field, max_size=(800, 300), quality=90):
    """Fungsi pembantu auto-resize gambar menggunakan Pillow tanpa merusak aspek rasio."""
    if not image_field:
        return
    name = getattr(image_field, 'name', '')
    ext = os.path.splitext(name)[1].lower()
    if ext in {'.svg', '.ico'}:
        return
    try:
        # Buka berkas dan cek dimensi
        image_field.seek(0)
        img = Image.open(image_field)
        if img.width > max_size[0] or img.height > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            output = io.BytesIO()
            fmt = 'PNG' if ext == '.png' else ('WEBP' if ext == '.webp' else 'JPEG')
            if fmt == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            img.save(output, format=fmt, quality=quality, optimize=True)
            output.seek(0)
            image_field.save(name, ContentFile(output.read()), save=False)
    except Exception:
        pass


class SiteSetting(models.Model):
    """
    Model konfigurasi situs utama berbasis pola Single Instance (Singleton).
    Menampung identitas situs, logo, footer, dan informasi kontak secara dinamis.
    """
    # 1. Identitas Situs & Header
    favicon = models.ImageField(
        upload_to='site/favicon/',
        blank=True,
        null=True,
        validators=[validate_favicon_file],
        help_text="Format .png, .ico, atau .svg (Rasio 1:1, ideal 64x64 atau 128x128 px, maks 500 KB)",
        verbose_name="Favicon Website"
    )
    header_logo = models.ImageField(
        upload_to='site/logo/',
        blank=True,
        null=True,
        validators=[validate_site_logo_file],
        help_text="Format .png, .webp, atau .svg transparan (Tinggi ideal 80–120 px, maks 2 MB)",
        verbose_name="Logo Header (Navbar)"
    )
    header_title = models.CharField(
        max_length=200,
        default="Administrasi Publik",
        verbose_name="Judul Header / Nama Instansi"
    )
    header_subtitle = models.CharField(
        max_length=200,
        default="FISIP Universitas Tadulako",
        verbose_name="Subjudul Header"
    )

    # 2. Pengaturan Footer
    footer_logo = models.ImageField(
        upload_to='site/logo/',
        blank=True,
        null=True,
        validators=[validate_site_logo_file],
        help_text="Format .png, .webp, atau .svg transparan (Tinggi ideal 80–120 px, maks 2 MB)",
        verbose_name="Logo Footer"
    )
    footer_title = models.CharField(
        max_length=200,
        default="Administrasi Publik",
        verbose_name="Judul Footer"
    )
    footer_subtitle = models.CharField(
        max_length=200,
        default="FISIP Universitas Tadulako",
        verbose_name="Subjudul Footer"
    )
    footer_description = models.TextField(
        default="Mencetak sarjana yang unggul, berintegritas, dan inovatif dalam perumusan kebijakan publik serta tata kelola pemerintahan yang berwawasan lingkungan.",
        verbose_name="Deskripsi Footer / Profil Singkat"
    )
    footer_short_address = models.CharField(
        max_length=255,
        default="Kampus Bumi Tadulako, Palu",
        verbose_name="Alamat Singkat Footer"
    )

    # 3. Kontak
    contact_title = models.CharField(
        max_length=200,
        default="Informasi Kontak",
        verbose_name="Judul Bagian Kontak"
    )
    contact_subtitle = models.CharField(
        max_length=200,
        default="Program Studi Administrasi Publik",
        verbose_name="Subjudul Bagian Kontak"
    )
    contact_address = models.TextField(
        default="Gedung FISIP UNTAD, Kampus Bumi Tadulako Tondo, Jl. Soekarno-Hatta Km. 9, Kota Palu, Sulawesi Tengah 94118",
        verbose_name="Alamat Lengkap"
    )
    contact_phone = models.CharField(
        max_length=50,
        default="(0451) 422611 / +62 811-450-000",
        verbose_name="Nomor Telepon Kantor"
    )
    contact_whatsapp = models.CharField(
        max_length=50,
        default="6285330144401",
        verbose_name="Nomor WhatsApp",
        help_text="Format 628xxx agar otomatis terhubung ke tombol WhatsApp publik (wa.me)"
    )
    contact_email = models.EmailField(
        default="admpublik@untad.ac.id",
        verbose_name="Alamat Email Resmi"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Pengaturan Situs (Site Settings)"
        verbose_name_plural = "Pengaturan Situs (Site Settings)"

    def __str__(self):
        return f"Pengaturan Situs: {self.header_title}"

    @property
    def clean_whatsapp(self):
        """Mengembalikan nomor telepon dalam digit murni diawali 628 untuk link wa.me."""
        if not self.contact_whatsapp:
            return "6285330144401"
        digits = re.sub(r'\D', '', str(self.contact_whatsapp))
        if digits.startswith('08'):
            digits = '628' + digits[2:]
        elif digits.startswith('8'):
            digits = '628' + digits[1:]
        return digits or "6285330144401"

    def save(self, *args, **kwargs):
        # Pola Singleton: Memastikan hanya ada 1 record konfigurasi dengan pk=1
        self.pk = 1

        # Auto-resize favicon (maks 256x256 px)
        if self.favicon:
            _resize_site_image(self.favicon, max_size=(256, 256))

        # Auto-resize logo header & footer (maks 800x300 px)
        if self.header_logo:
            _resize_site_image(self.header_logo, max_size=(800, 300))
        if self.footer_logo:
            _resize_site_image(self.footer_logo, max_size=(800, 300))

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Mencegah penghapusan instance utama konfigurasi
        pass

    @classmethod
    def get_settings(cls):
        """Metode aman untuk mendapatkan instance pengaturan dengan fallback otomatis."""
        obj, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'header_title': 'Administrasi Publik',
                'header_subtitle': 'FISIP Universitas Tadulako',
                'footer_title': 'Administrasi Publik',
                'footer_subtitle': 'FISIP Universitas Tadulako',
                'footer_description': 'Mencetak sarjana yang unggul, berintegritas, dan inovatif dalam perumusan kebijakan publik serta tata kelola pemerintahan yang berwawasan lingkungan.',
                'footer_short_address': 'Kampus Bumi Tadulako, Palu',
                'contact_title': 'Informasi Kontak',
                'contact_subtitle': 'Program Studi Administrasi Publik',
                'contact_address': 'Gedung FISIP UNTAD, Kampus Bumi Tadulako Tondo, Jl. Soekarno-Hatta Km. 9, Kota Palu, Sulawesi Tengah 94118',
                'contact_email': 'admpublik@untad.ac.id',
                'contact_phone': '(0451) 422611 / +62 811-450-000',
                'contact_whatsapp': '6285330144401',
            }
        )
        return obj


class SocialMedia(models.Model):
    """
    Model relasi akun media sosial resmi prodi.
    Hanya ditampilkan jika URL terisi dan berstatus aktif.
    """
    site_setting = models.ForeignKey(
        SiteSetting,
        on_delete=models.CASCADE,
        related_name='social_medias',
        verbose_name="Pengaturan Situs"
    )
    platform = models.CharField(
        max_length=30,
        choices=SOCIAL_PLATFORM_CHOICES,
        verbose_name="Platform Media Sosial"
    )
    url = models.URLField(
        blank=True,
        null=True,
        verbose_name="Tautan / URL Akun",
        help_text="Contoh: https://instagram.com/admpublik_untad (kosongkan jika tidak dipakai)"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Urutan Tampil",
        help_text="Urutan urut posisi ikon (0, 1, 2...)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Status Aktif",
        help_text="Hilangkan centang jika ingin menyembunyikan sementara dari pengunjung"
    )

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Sosial Media"
        verbose_name_plural = "Sosial Media"

    def __str__(self):
        return f"{self.get_platform_display()} ({self.url or 'Tanpa URL'})"

    def get_icon_class(self):
        """Ikon Bootstrap Icons bawaan sistem."""
        return PLATFORM_ICONS.get(self.platform, 'bi bi-globe')

    def get_fa_icon_class(self):
        """Ikon Font Awesome bawaan sistem."""
        return PLATFORM_FA_ICONS.get(self.platform, 'fas fa-globe')


class QuickLink(models.Model):
    """
    Model relasi tautan cepat pada footer / halaman portal (Layanan & Portal).
    Mendukung tautan URL internal/eksternal maupun unggahan berkas (PDF).
    """
    site_setting = models.ForeignKey(
        SiteSetting,
        on_delete=models.CASCADE,
        related_name='quick_links',
        verbose_name="Pengaturan Situs"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Judul Tautan",
        help_text="Contoh: Portal SIGA-8, Website UNTAD, Sertifikat Akreditasi"
    )
    url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Tautan URL",
        help_text="Tautan website (https://...) atau path internal website (/akademik/kurikulum/)"
    )
    file = models.FileField(
        upload_to='site/quick_links/',
        blank=True,
        null=True,
        validators=[validate_document_file],
        verbose_name="Unggah Berkas / Dokumen",
        help_text="Pilihan jika tautan berupa dokumen unduhan (misal: PDF Akreditasi)"
    )
    open_in_new_tab = models.BooleanField(
        default=True,
        verbose_name="Buka di Tab Baru",
        help_text="Centang agar terbuka di tab baru (_blank)"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Urutan Tampil",
        help_text="Urutan tampil pada daftar tautan cepat"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Status Aktif",
        help_text="Centang agar tampil di website publik"
    )

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Tautan Cepat"
        verbose_name_plural = "Tautan Cepat"

    def __str__(self):
        return self.title

    def get_url(self):
        if self.file:
            return self.file.url
        return self.url or '#'

    @property
    def is_file(self):
        return bool(self.file)


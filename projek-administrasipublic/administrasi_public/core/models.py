from django.db import models
from django.utils import timezone
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field  # type: ignore


# 1. Model Sambutan Koordinator Prodi (Menggunakan CKEditor 5)
class Sambutan(models.Model):
    judul = models.CharField(max_length=200, default="Sambutan Koordinator Prodi")
    isi = CKEditor5Field('Isi Sambutan', config_name='extends')
    nama_author = models.CharField(max_length=150, verbose_name="Nama Pimpinan / Koordinator")
    foto = models.ImageField(upload_to='sambutan/', blank=True, null=True, help_text="Upload foto resmi koordinator prodi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Sambutan Koordinator Prodi"
        verbose_name_plural = "Sambutan Koordinator Prodi"

    def __str__(self):
        return f"{self.judul} - {self.nama_author}"


# 2. Model Galeri Kegiatan
class Galeri(models.Model):
    judul = models.CharField(max_length=200)
    gambar = models.ImageField(upload_to='galeri/', blank=True, null=True, help_text="Upload gambar dokumentasi kegiatan")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Galeri Kegiatan"
        verbose_name_plural = "Galeri Kegiatan"

    def __str__(self):
        return self.judul


# 3. Model Berita (Konten menggunakan CKEditor 5)
class Berita(models.Model):
    judul = models.CharField(max_length=255)
    ringkasan = models.TextField(blank=True, null=True)
    konten = CKEditor5Field('Konten Berita', config_name='extends')
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True, help_text="Upload foto/gambar berita")
    posted_at = models.DateTimeField(default=timezone.now, verbose_name="Waktu Tayang / Post")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Waktu Diperbarui")

    class Meta:
        verbose_name = "Berita"
        verbose_name_plural = "Daftar Berita"
        ordering = ['-posted_at']

    def __str__(self):
        return self.judul


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

    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='DOSEN')
    nama = models.CharField(max_length=200, help_text="Nama lengkap beserta gelar")
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES, default='L', verbose_name="Jenis Kelamin")
    bidang_ilmu = models.CharField(max_length=200, verbose_name="Bidang Ilmu / Jabatan")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DOSEN TETAP')
    foto = models.ImageField(upload_to='pegawai/', blank=True, null=True, help_text="Upload foto rasio 1:1")

    # Identitas Kepegawaian (blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIDN")
    nip = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIP")
    nuptk = models.CharField(max_length=50, blank=True, null=True, verbose_name="NUPTK")
    no_hp = models.CharField(max_length=30, blank=True, null=True, verbose_name="No. HP / WhatsApp")

    # Relasi ForeignKey ke tabel PangkatGolongan
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


# 7. Model Halaman Tentang (Profil, Sejarah, Struktur)
class HalamanTentang(models.Model):
    KATEGORI_CHOICES = [
        ('profil', 'Profil Program Studi'),
        ('sejarah', 'Sejarah Singkat'),
        ('struktur', 'Struktur Organisasi'),
    ]
    kategori = models.CharField(max_length=50, choices=KATEGORI_CHOICES, unique=True)
    judul = models.CharField(max_length=255)
    isi = CKEditor5Field('Isi Konten', config_name='extends')
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
    isi = CKEditor5Field('Isi Konten Akademik', config_name='extends')
    link_eksternal = models.URLField(blank=True, null=True, verbose_name="Tautan Eksternal / Portal")
    file_utama = models.FileField(upload_to='akademik/dokumen/', blank=True, null=True, verbose_name="Dokumen Utama (PDF/Excel)")
    nama_file_utama = models.CharField(max_length=150, blank=True, null=True, verbose_name="Label Tombol Unduh", help_text="Contoh: Unduh Kurikulum Lengkap (PDF)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Terakhir Diperbarui")

    class Meta:
        verbose_name = "Halaman Akademik"
        verbose_name_plural = "Daftar Halaman Akademik"
        ordering = ['id']

    def __str__(self):
        return self.get_kategori_display()


# 10. Model Berkas / Lampiran Tambahan untuk Halaman Akademik
class DokumenAkademik(models.Model):
    halaman = models.ForeignKey(HalamanAkademik, on_delete=models.CASCADE, related_name='dokumen_list', verbose_name="Halaman Terkait")
    judul = models.CharField(max_length=255, verbose_name="Nama Dokumen / Berkas")
    file = models.FileField(upload_to='akademik/berkas/', verbose_name="Upload File (PDF/Doc/Xls)")
    keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan Singkat")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Unggah")

    class Meta:
        verbose_name = "Dokumen / Berkas Akademik"
        verbose_name_plural = "Daftar Dokumen Akademik"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.judul} ({self.halaman.get_kategori_display()})"

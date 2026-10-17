from django.db import models
from django.utils import timezone
from django.conf import settings

# Model untuk data section Sambutan Koordinator Prodi
class Sambutan(models.Model):
    judul = models.CharField(max_length=200, default="Sambutan Koordinator Prodi")
    isi = models.TextField()
    nama_author = models.CharField(max_length=150)
    foto = models.CharField(max_length=255, default="foto1.jpg")

    def __str__(self):
        return self.judul


# Model untuk data section Galeri Kegiatan
class Galeri(models.Model):
    judul = models.CharField(max_length=200)
    gambar = models.CharField(max_length=255)

    def __str__(self):
        return self.judul


# Model Berita
class Berita(models.Model):
    judul = models.CharField(max_length=255)
    ringkasan = models.TextField(blank=True, null=True)
    konten = models.TextField(blank=True, null=True)
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True, help_text="Upload foto/gambar berita")
    
    posted_at = models.DateTimeField(default=timezone.now, verbose_name="Waktu Tayang / Post")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Waktu Diperbarui")

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return self.judul


# Model Tenaga Pendidik & Kependidikan (Dibedakan lewat field jenis)
class TenagaPendidik(models.Model):
    JENIS_CHOICES = [
        ('DOSEN', 'Dosen Pengajar'),
        ('TENDIK', 'Tenaga Kependidikan'),
    ]

    STATUS_CHOICES = [
        ('DOSEN TETAP', 'DOSEN TETAP'),
        ('DOSEN LUAR BIASA', 'DOSEN LUAR BIASA'),
        ('PROFESOR', 'PROFESOR'),
        ('STAF ADMINISTRASI', 'STAF ADMINISTRASI'),
        ('KEPALA TATA USAHA', 'KEPALA TATA USAHA'),
    ]

    # Pemisah Dosen dan Tendik
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='DOSEN')

    # Data Depan Kartu
    nama = models.CharField(max_length=200, help_text="Nama lengkap beserta gelar")
    bidang_ilmu = models.CharField(max_length=200, verbose_name="Bidang Ilmu / Jabatan")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DOSEN TETAP')
    foto = models.ImageField(upload_to='dosen/', blank=True, null=True, help_text="Upload foto rasio 1:1")

    # Data Belakang Kartu
    email = models.EmailField(blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIDN")
    nip = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIP")
    no_hp = models.CharField(max_length=30, blank=True, null=True, verbose_name="No. HP / WhatsApp")
    pangkat_gol = models.CharField(max_length=150, blank=True, null=True, verbose_name="Pangkat / Golongan")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tenaga Pendidik & Kependidikan"
        verbose_name_plural = "Tenaga Pendidik & Kependidikan"
        ordering = ['nama']

    def __str__(self):
        return f"{self.nama} ({self.jenis})"


# Model Audit Log (Pencatat Riwayat Aktivitas & Riwayat Login Admin)
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
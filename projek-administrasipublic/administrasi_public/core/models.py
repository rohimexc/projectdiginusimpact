from django.db import models
from django.utils import timezone

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


# Model untuk data section Berita Terbaru (Sudah disesuaikan revisi mentor)
class Berita(models.Model):
    judul = models.CharField(max_length=255)
    ringkasan = models.TextField(blank=True, null=True)
    konten = models.TextField(blank=True, null=True)
    gambar = models.CharField(max_length=255, blank=True, null=True, default="https://placehold.co/600x400")
    
    # 3 field datetime yang diminta mentor
    posted_at = models.DateTimeField(default=timezone.now, verbose_name="Waktu Tayang / Post")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Dibuat")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Waktu Diperbarui")

    class Meta:
        # Urutan otomatis agar berita dengan post terbaru tampil paling atas
        ordering = ['-posted_at']

    def __str__(self):
        return self.judul


# Model untuk data Halaman Tenaga Pendidik / Staf Dosen
class TenagaPendidik(models.Model):
    STATUS_CHOICES = [
        ('DOSEN TETAP', 'DOSEN TETAP'),
        ('DOSEN LUAR BIASA', 'DOSEN LUAR BIASA'),
        ('PROFESOR', 'PROFESOR'),
    ]

    # Data Tampak Depan Kartu
    nama = models.CharField(max_length=200, help_text="Nama lengkap beserta gelar (cth: Dr. Ahmad Fauzi, M.Si)")
    bidang_ilmu = models.CharField(max_length=200, help_text="Bidang keilmuan / kepakaran (cth: Kebijakan Publik)")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='DOSEN TETAP')
    
    # Foto: Menggunakan ImageField agar bisa browse/pilih file dari folder laptop (rasio 1:1)
    foto = models.ImageField(
        upload_to='dosen/',
        blank=True,
        null=True,
        help_text="Upload foto dosen (disarankan rasio 1:1 / persegi)"
    )

    # Data Tampak Belakang Kartu (Muncul saat di-hover)
    email = models.EmailField(blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIDN")
    nip = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIP")
    no_hp = models.CharField(max_length=30, blank=True, null=True, verbose_name="No. HP / WhatsApp")
    pangkat_gol = models.CharField(max_length=150, blank=True, null=True, verbose_name="Pangkat / Golongan", help_text="cth: Lektor Kepala / IV-a atau Guru Besar / IV-d")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tenaga Pendidik"
        verbose_name_plural = "Tenaga Pendidik"
        ordering = ['nama']

    def __str__(self):
        return self.nama
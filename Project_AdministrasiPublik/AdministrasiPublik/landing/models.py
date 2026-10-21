from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.utils.text import slugify

class Sambutan(models.Model):
    judul = models.CharField(max_length=200, default="Sambutan Koordinator Prodi")
    nama_koor = models.CharField(max_length=150, default="Dr. Intam Kurnia, M.Si.")
    isi_sambutan = models.TextField()

    def __str__(self):
        return self.judul

class Galeri(models.Model):
    judul = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='images/galeri/')
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.judul

class Berita(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True) # Pastikan field ini ada
    konten = CKEditor5Field('Konten', config_name='extends')
    post_date = models.DateTimeField(auto_now_add=True)
    
    # Sesuai permintaan: datetime create, update, dan post untuk pengurutan
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_date = models.DateTimeField(help_text="Tanggal dan waktu publikasi berita")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

    class Meta:
        ordering = ['-post_date'] # Urutkan otomatis berdasarkan post terbaru
class Akademik(models.Model):
    judul_informasi = models.CharField(max_length=200)
    deskripsi = models.TextField()
    file_dokumen = models.FileField(upload_to='documents/akademik/', blank=True, null=True)

    def __str__(self):
        return self.judul_informasi

class TenagaPendidik(models.Model):
    nama = models.CharField(max_length=255)
    jk = models.CharField(max_length=1, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    kategori = models.CharField(max_length=100, blank=True, null=True) # Bidang Ilmu / Unit Kerja
    status = models.CharField(max_length=100, blank=True, null=True)    # Status Kepegawaian
    pangkat = models.CharField(max_length=150, blank=True, null=True)   # Pangkat / Golongan
    email = models.EmailField(blank=True, null=True)
    nip = models.CharField(max_length=50, blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True)
    telepon = models.CharField(max_length=30, blank=True, null=True)
    foto = models.ImageField(upload_to='tenaga_tendik/', blank=True, null=True)

    def __str__(self):
        return self.nama

class Akreditasi(models.Model):
    status_akreditasi = models.CharField(max_length=50, default="Unggul (A)")
    nomor_sk = models.CharField(max_length=100)
    tanggal_kadaluarsa = models.DateField()
    sertifikat = models.FileField(upload_to='documents/akreditasi/', blank=True, null=True)

    def __str__(self):
        return f"Akreditasi {self.status_akreditasi}"

class Kontak(models.Model):
    alamat = models.TextField()
    telepon = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return "Informasi Kontak Prodi"

class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aktivitas = models.TextField()
    
    # --- TAMBAHKAN DUA BARIS INI ---
    keterangan = models.CharField(max_length=255, default="-", blank=True, null=True)
    ip_address = models.CharField(max_length=50, default="-", blank=True, null=True)
    # -----------------------------
    
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.aktivitas} pada {self.waktu}"
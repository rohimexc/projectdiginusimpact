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
from django.db import models

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

# Model untuk data section Berita Terbaru
class Berita(models.Model):
    judul = models.CharField(max_length=255)
    ringkasan = models.TextField(blank=True, null=True)
    gambar = models.CharField(max_length=255, blank=True, null=True)
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.judul
from django.db import models

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
    konten = models.TextField()
    gambar = models.ImageField(upload_to='images/berita/')
    tanggal = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.judul

class Akademik(models.Model):
    judul_informasi = models.CharField(max_length=200)
    deskripsi = models.TextField()
    file_dokumen = models.FileField(upload_to='documents/akademik/', blank=True, null=True)

    def __str__(self):
        return self.judul_informasi

class StafDosen(models.Model):
    nama = models.CharField(max_length=150)
    jabatan = models.CharField(max_length=100)
    nip_nidn = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='images/staf/')

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
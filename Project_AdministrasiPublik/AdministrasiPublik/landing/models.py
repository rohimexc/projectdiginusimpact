from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.auth.models import User
from django.utils.text import slugify


class TentangPage(models.Model):
    judul = models.CharField(max_length=150, verbose_name="Nama Menu / Sub-Menu")
    slug = models.SlugField(max_length=100, unique=True, help_text="Slug URL sub-menu (misal: profil, sejarah, visi, tujuan, profil-lulusan, sertifikat)")
    konten = CKEditor5Field(blank=True, null=True, verbose_name="Isi Konten", config_name='extends')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Konten Menu Tentang"
        verbose_name_plural = "Konten Menu Tentang"
        ordering = ['id']

    def __str__(self):
        return self.judul

class VisiMisiTujuan(models.Model):
    visi = models.TextField(
        verbose_name="Teks Visi",
        help_text="Teks visi utama program studi"
    )
    pengantar_misi = models.CharField(
        max_length=255,
        default="Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki misi sebagai berikut:",
        verbose_name="Kalimat Pengantar Misi"
    )
    pengantar_tujuan = models.CharField(
        max_length=255,
        default="Program Studi Administrasi Publik FISIP Universitas Tadulako memiliki tujuan Pendidikan berupa:",
        verbose_name="Kalimat Pengantar Tujuan"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visi, Misi & Tujuan (Pengaturan)"
        verbose_name_plural = "Visi, Misi & Tujuan (Pengaturan)"

    def __str__(self):
        return "Pengaturan Visi, Misi dan Tujuan"


class MisiItem(models.Model):
    visi_misi = models.ForeignKey(VisiMisiTujuan, on_delete=models.CASCADE, related_name='misi_items', null=True, blank=True)
    urutan = models.PositiveIntegerField(default=1, verbose_name="Nomor Urut")
    deskripsi = models.TextField(verbose_name="Isi Misi")

    class Meta:
        verbose_name = "Item Misi"
        verbose_name_plural = "Daftar Item Misi"
        ordering = ['urutan', 'id']

    def __str__(self):
        return f"Misi {self.urutan}: {self.deskripsi[:50]}..."


class TujuanItem(models.Model):
    visi_misi = models.ForeignKey(VisiMisiTujuan, on_delete=models.CASCADE, related_name='tujuan_items', null=True, blank=True)
    urutan = models.PositiveIntegerField(default=1, verbose_name="Nomor Urut")
    judul = models.CharField(max_length=200, verbose_name="Judul Tujuan", help_text="Contoh: Employabilitas, Reputasi Akademik, dll.")
    subjudul = models.CharField(max_length=200, blank=True, null=True, verbose_name="Subjudul / Terjemahan (Opsional)", help_text="Contoh: Employability, Academic Reputation (opsional)")
    deskripsi = models.TextField(verbose_name="Deskripsi Tujuan")

    class Meta:
        verbose_name = "Item Tujuan"
        verbose_name_plural = "Daftar Item Tujuan"
        ordering = ['urutan', 'id']

    def __str__(self):
        return f"Tujuan {self.urutan}: {self.judul}"


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
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True)
    konten = CKEditor5Field('Konten', config_name='extends')
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
        ordering = ['-post_date']

class Akademik(models.Model):
    judul_informasi = models.CharField(max_length=200)
    deskripsi = models.TextField()
    file_dokumen = models.FileField(upload_to='documents/akademik/', blank=True, null=True)

    def __str__(self):
        return self.judul_informasi


class AkademikPage(models.Model):
    judul = models.CharField(max_length=150, verbose_name="Nama Sub-Menu Akademik")
    slug = models.SlugField(max_length=100, unique=True, help_text="Slug URL sub-menu (misal: siga-8, kurikulum, jadwal-perkuliahan, rps, panduan-akademik)")
    subjudul = models.CharField(max_length=255, blank=True, null=True, verbose_name="Subjudul / Keterangan Singkat")
    link_eksternal = models.URLField(max_length=500, blank=True, null=True, verbose_name="Tautan Eksternal / Portal (Opsional)", help_text="Misal: https://siga.untad.ac.id")
    file_utama = models.FileField(upload_to='documents/akademik/', blank=True, null=True, verbose_name="File Dokumen Utama (PDF/Doc)")
    konten = CKEditor5Field(blank=True, null=True, verbose_name="Isi Konten", config_name='extends')
    urutan = models.PositiveIntegerField(default=1, verbose_name="Nomor Urutan Tampil")
    is_active = models.BooleanField(default=True, verbose_name="Status Aktif")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sub-Menu Akademik"
        verbose_name_plural = "Sub-Menu Akademik"
        ordering = ['urutan', 'id']

    def __str__(self):
        return self.judul


class DokumenAkademik(models.Model):
    akademik = models.ForeignKey(AkademikPage, on_delete=models.CASCADE, related_name='dokumen_list', verbose_name="Sub-Menu Akademik")
    judul = models.CharField(max_length=200, verbose_name="Nama Dokumen / Berkas")
    file = models.FileField(upload_to='documents/akademik/lampiran/', verbose_name="File Berkas")
    keterangan = models.CharField(max_length=255, blank=True, null=True, verbose_name="Keterangan")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Dokumen Pendukung Akademik"
        verbose_name_plural = "Daftar Dokumen Pendukung Akademik"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.akademik.judul} - {self.judul}"

class TenagaPendidik(models.Model):
    nama = models.CharField(max_length=255)
    jk = models.CharField(max_length=1, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    kategori = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    pangkat = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    nip = models.CharField(max_length=50, blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True)
    telepon = models.CharField(max_length=30, blank=True, null=True)
    foto = models.ImageField(upload_to='tenaga_tendik/', blank=True, null=True)

    def __str__(self):
        return self.nama

PANGKAT_GOLONGAN_CHOICES = [
    ('', '--- Pilih Pangkat / Golongan ---'),
    ('III/a', 'III/a - Penata Muda'),
    ('III/b', 'III/b - Penata Muda Tingkat I'),
    ('III/c', 'III/c - Penata'),
    ('III/d', 'III/d - Penata Tingkat I'),
    ('IV/a', 'IV/a - Pembina'),
    ('IV/b', 'IV/b - Pembina Tingkat I'),
    ('IV/c', 'IV/c - Pembina Utama Muda'),
    ('IV/d', 'IV/d - Pembina Utama Madya'),
    ('IV/e', 'IV/e - Pembina Utama'),
]

STATUS_KEPEGAWAIAN_CHOICES = [
    ('', '--- Pilih Status Kepegawaian ---'),
    ('Dosen Tetap', 'Dosen Tetap'),
    ('Dosen Tetap Yayasan', 'Dosen Tetap Yayasan'),
    ('Dosen Luar Biasa', 'Dosen Luar Biasa'),
    ('Dosen PNS', 'Dosen PNS'),
    ('Dosen PPPK', 'Dosen PPPK'),
]

class Dosen(models.Model):
    nama = models.CharField(max_length=200)
    nip = models.CharField(max_length=50, blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True)
    nuptk = models.CharField(max_length=50, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=1, choices=[('', '--- Pilih Jenis Kelamin ---'), ('L', 'Laki-laki'), ('P', 'Perempuan')], blank=True, null=True)
    bidang_ilmu = models.CharField(max_length=150, blank=True, null=True)
    jabatan = models.CharField(max_length=100, blank=True, null=True)
    pangkat_golongan = models.CharField(max_length=50, choices=PANGKAT_GOLONGAN_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_KEPEGAWAIAN_CHOICES, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    no_hp = models.CharField(max_length=30, blank=True, null=True)
    foto = models.ImageField(upload_to='dosen/', blank=True, null=True)

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
    keterangan = models.CharField(max_length=255, default="-", blank=True, null=True)
    ip_address = models.CharField(max_length=50, default="-", blank=True, null=True)
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.aktivitas} pada {self.waktu}"
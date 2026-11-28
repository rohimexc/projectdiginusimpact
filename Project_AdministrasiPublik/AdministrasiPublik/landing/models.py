from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.text import slugify


def validate_video_file_size(value):
    max_size = 100 * 1024 * 1024  # 100 MB
    if value.size > max_size:
        raise ValidationError("Ukuran file video tidak boleh melebihi 100 MB.")


def validate_image_file_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB
    if value.size > max_size:
        raise ValidationError("Ukuran file gambar tidak boleh melebihi 5 MB.")


def validate_document_file_size(value):
    max_size = 10 * 1024 * 1024  # 10 MB
    if value.size > max_size:
        raise ValidationError("Ukuran berkas dokumen tidak boleh melebihi 10 MB.")
from django_ckeditor_5.fields import CKEditor5Field


class TentangPage(models.Model):
    judul = models.CharField(max_length=150, verbose_name="Nama Menu / Sub-Menu")
    slug = models.SlugField(max_length=100, unique=True, help_text="Slug URL sub-menu (misal: profil, sejarah, visi, tujuan, profil-lulusan, sertifikat)")
    file_dokumen = models.FileField(upload_to='documents/tentang/', blank=True, null=True, verbose_name="File Berkas / Sertifikat (PDF/Gambar)")
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
    judul = models.CharField(max_length=200, blank=True, null=True, verbose_name="Judul / Keterangan Foto")
    foto = models.ImageField(
        upload_to='images/galeri/', 
        verbose_name="Foto Galeri",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_image_file_size
        ]
    )
    urutan = models.PositiveIntegerField(default=1, verbose_name="Urutan Tampil")
    tanggal = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Galeri Foto"
        verbose_name_plural = "Daftar Galeri Foto"
        ordering = ['urutan', '-tanggal', '-id']

    def __str__(self):
        return self.judul or f"Foto Galeri #{self.id}"


class Hero(models.Model):
    video_url = models.CharField(
        max_length=500, 
        blank=True, 
        null=True, 
        verbose_name="Link Video",
        help_text="Link video banner (misal: /static/video/banner.mp4 atau URL video)"
    )
    video_file = models.FileField(
        upload_to='hero/videos/',
        blank=True,
        null=True,
        verbose_name="Upload File Video",
        help_text="File video hero (Maksimal 100 MB, format: MP4, WebM)",
        validators=[
            FileExtensionValidator(allowed_extensions=['mp4', 'webm']),
            validate_video_file_size
        ]
    )
    foto = models.ImageField(
        upload_to='hero/', 
        blank=True, 
        null=True, 
        verbose_name="Upload Gambar Hero",
        help_text="Gambar hero yang tampil langsung saat video masih dimuat (Maksimal 5 MB, format: JPG, JPEG, PNG, WEBP)",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp']),
            validate_image_file_size
        ]
    )
    judul = models.CharField(
        max_length=200, 
        default="Administrasi Publik", 
        blank=True, 
        null=True, 
        verbose_name="Judul Hero"
    )
    subjudul = models.CharField(
        max_length=255, 
        default="Welcome to", 
        blank=True, 
        null=True, 
        verbose_name="Subjudul / Teks Atas"
    )
    deskripsi = models.TextField(
        default="Fakultas Ilmu Sosial dan Ilmu Politik\nUniversitas Tadulako", 
        blank=True, 
        null=True, 
        verbose_name="Deskripsi Hero"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Status Aktif",
        help_text="Centang untuk menampilkan hero ini di halaman utama"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_video_source(self):
        if self.video_file:
            return self.video_file.url
        return self.video_url or ""

    class Meta:
        verbose_name = "Hero Banner"
        verbose_name_plural = "Hero Banner"
        ordering = ['-is_active', '-updated_at', '-id']

    def __str__(self):
        return f"Hero: {self.judul or self.video_url or self.id}"

class Berita(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True)
    konten = CKEditor5Field('Konten', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post_date = models.DateTimeField(help_text="Tanggal dan waktu publikasi berita")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Jumlah Dilihat")
    shares_count = models.PositiveIntegerField(default=0, verbose_name="Jumlah Dibagikan")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_komentar(self):
        return self.komentar_list.filter(is_active=True).count()

    def __str__(self):
        return self.judul

    class Meta:
        ordering = ['-post_date']

class LikeBerita(models.Model):
    berita = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='likes', verbose_name="Berita")
    session_key = models.CharField(max_length=100, db_index=True, verbose_name="Kunci Sesi Pengunjung")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Alamat IP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Disukai")

    class Meta:
        verbose_name = "Like Berita"
        verbose_name_plural = "Daftar Like Berita"
        unique_together = ('berita', 'session_key')
        ordering = ['-created_at']

    def __str__(self):
        return f"Like oleh {self.session_key} pada {self.berita.judul}"


class KomentarBerita(models.Model):
    berita = models.ForeignKey(Berita, on_delete=models.CASCADE, related_name='komentar_list', verbose_name="Berita")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='komentar_berita', verbose_name="Pengguna")
    nama = models.CharField(max_length=100, verbose_name="Nama Pengunjung")
    email = models.EmailField(blank=True, null=True, verbose_name="Email (Opsional)")
    isi = models.TextField(verbose_name="Isi Komentar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Komentar")
    is_active = models.BooleanField(default=True, verbose_name="Status Tampil")

    class Meta:
        verbose_name = "Komentar Berita"
        verbose_name_plural = "Daftar Komentar Berita"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.nama} pada {self.berita.judul}"


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

JABATAN_DOSEN_CHOICES = [
    ('', '--- Pilih Jabatan / Posisi Dosen ---'),
    ('Dosen Tetap', 'Dosen Tetap'),
    ('Dosen Pengajar', 'Dosen Pengajar'),
    ('Ketua Program Studi', 'Ketua Program Studi (Kaprodi)'),
    ('Sekretaris Program Studi', 'Sekretaris Program Studi (Sekprodi)'),
    ('Kepala Laboratorium', 'Kepala Laboratorium'),
    ('Dosen Luar Biasa', 'Dosen Luar Biasa'),
    ('Profesor', 'Profesor'),
]

class Dosen(models.Model):
    nama = models.CharField(max_length=200)
    nip = models.CharField(max_length=50, blank=True, null=True)
    nidn = models.CharField(max_length=50, blank=True, null=True)
    nuptk = models.CharField(max_length=50, blank=True, null=True)
    jenis_kelamin = models.CharField(max_length=1, choices=[('', '--- Pilih Jenis Kelamin ---'), ('L', 'Laki-laki'), ('P', 'Perempuan')], blank=True, null=True)
    bidang_ilmu = models.CharField(max_length=150, blank=True, null=True)
    jabatan = models.CharField(max_length=100, choices=JABATAN_DOSEN_CHOICES, blank=True, null=True)
    pangkat_golongan = models.CharField(max_length=50, choices=PANGKAT_GOLONGAN_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_KEPEGAWAIAN_CHOICES, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    no_hp = models.CharField(max_length=30, blank=True, null=True)
    foto = models.ImageField(upload_to='dosen/', blank=True, null=True)

    def __str__(self):
        return self.nama

class Akreditasi(models.Model):
    status_akreditasi = models.CharField(max_length=50, default="Unggul (A)")
    nomor_sk = models.CharField(max_length=100, blank=True, null=True, default="-")
    tanggal_kadaluarsa = models.DateField(blank=True, null=True)
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


class PengunjungWeb(models.Model):
    tanggal = models.DateField(default=timezone.localdate, db_index=True)
    ip_address = models.CharField(max_length=50, blank=True, null=True)
    session_key = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pengunjung Web"
        verbose_name_plural = "Daftar Pengunjung Web"
        unique_together = ('tanggal', 'session_key')

    def __str__(self):
        return f"{self.tanggal} - {self.session_key or self.ip_address}"


class EventTerdekat(models.Model):
    nama_mahasiswa = models.CharField(max_length=200, verbose_name="Nama Mahasiswa / Judul Event")
    nim = models.CharField(max_length=50, blank=True, null=True, verbose_name="NIM (Opsional)", help_text="Contoh: G81122014")
    kategori = models.CharField(max_length=100, default="Komprehensif", verbose_name="Kategori / Jenis Event", help_text="Contoh: Komprehensif, Seminar Proposal, Seminar Hasil, Yudisium, dll.")
    tanggal_event = models.DateField(verbose_name="Tanggal Event", help_text="Pilih tanggal pelaksanaan event")
    hari_tanggal_manual = models.CharField(max_length=150, blank=True, null=True, verbose_name="Teks Tanggal Manual (Opsional)", help_text="Biarkan kosong jika ingin otomatis diformat, misal: 'Rabu 24 Juni 2026'")
    waktu = models.CharField(max_length=100, blank=True, null=True, verbose_name="Waktu Pelaksanaan (Opsional)", help_text="Contoh: 09:00 WITA - Selesai")
    lokasi = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lokasi / Ruangan (Opsional)", help_text="Contoh: Ruang Ujian Jurusan / Daring")
    poster = models.ImageField(upload_to='event_terdekat/', verbose_name="Poster Flyer (Format Gambar)", validators=[validate_image_file_size])
    urutan = models.PositiveIntegerField(default=1, verbose_name="Nomor Urut Tampil")
    is_active = models.BooleanField(default=True, verbose_name="Aktif / Tampilkan di Beranda")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event Terdekat"
        verbose_name_plural = "Daftar Event Terdekat"
        ordering = ['urutan', 'tanggal_event', 'id']

    def __str__(self):
        if self.nim:
            return f"{self.nama_mahasiswa} ({self.nim}) - {self.kategori}"
        return f"{self.nama_mahasiswa} - {self.kategori}"

    @property
    def label_peserta(self):
        if self.nim:
            return f"{self.nama_mahasiswa} ({self.nim})"
        return self.nama_mahasiswa

    @property
    def display_tanggal(self):
        if self.hari_tanggal_manual:
            return self.hari_tanggal_manual
        if self.tanggal_event:
            hari_list = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
            bulan_list = ['', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
            nama_hari = hari_list[self.tanggal_event.weekday()]
            nama_bulan = bulan_list[self.tanggal_event.month]
            return f"{nama_hari} {self.tanggal_event.day} {nama_bulan} {self.tanggal_event.year}"
        return "-"

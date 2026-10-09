from django.db import models
from django.contrib.auth.models import AbstractUser

# Model Pengguna Kustom (Mendukung RBAC & Status Akun)
class User(AbstractUser):
    class Role(models.TextChoices):
        SUPERADMIN = 'SUPERADMIN', 'Super Admin'
        ADMIN = 'ADMIN', 'Admin Prodi'
        DOSEN = 'DOSEN', 'Dosen'
        MAHASISWA = 'MAHASISWA', 'Mahasiswa'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MAHASISWA,
        verbose_name="Peran / Role"
    )
    nomor_telepon = models.CharField(max_length=15, blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    # is_active, date_joined, username, email otomatis tersedia dari AbstractUser

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Model Audit Log untuk Mencatat Aktivitas Pengguna (Tahap 3)
class AuditLog(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='audit_logs'
    )
    aksi = models.CharField(max_length=100) # Contoh: Tambah User, Ubah Role, Nonaktifkan Akun
    deskripsi = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-waktu']

    def __str__(self):
        return f"[{self.waktu.strftime('%d-%m-%Y %H:%M')}] {self.user} - {self.aksi}"
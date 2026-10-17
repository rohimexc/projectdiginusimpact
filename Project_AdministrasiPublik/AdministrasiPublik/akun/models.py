from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Operator', 'Operator'), ('Dosen', 'Dosen')], default='Operator')
    foto = models.ImageField(upload_to='images/user/', blank=True, null=True)
    no_telepon = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    # Model untuk mencatat riwayat login user
class RiwayatLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu_login = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.waktu_login}"

# Model untuk mencatat aktivitas/audit log admin (Tambah, Edit, Hapus data)
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    aktivitas = models.CharField(max_length=255)
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.waktu}] {self.user.username if self.user else 'Sistem'} - {self.aktivitas}"
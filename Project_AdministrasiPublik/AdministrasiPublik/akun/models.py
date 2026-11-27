from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Operator', 'Operator'), ('Dosen', 'Dosen'), ('USER', 'USER')], default='USER')
    foto = models.ImageField(upload_to='images/user/', blank=True, null=True)
    no_telepon = models.CharField(max_length=20, blank=True, null=True)
    raw_password = models.CharField(max_length=128, blank=True, null=True, verbose_name="Password (Plain)")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'Admin' if instance.is_superuser else 'USER'
        UserProfile.objects.get_or_create(user=instance, defaults={'role': role})
    # Model untuk mencatat riwayat login user
class RiwayatLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    waktu_login = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.waktu_login}"

# Model untuk mencatat rekam jejak aktivitas admin/sistem
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='akun_auditlogs')
    aktivitas = models.TextField()
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Sistem"
        return f"[{self.waktu}] {username}: {self.aktivitas}"

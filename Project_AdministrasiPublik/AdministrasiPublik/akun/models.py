from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('Admin', 'Admin'), ('Operator', 'Operator'), ('Dosen', 'Dosen')], default='Operator')
    foto = models.ImageField(upload_to='images/user/', blank=True, null=True)
    no_telepon = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Form untuk Create (Add) Akun Pengguna Baru
class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'nomor_telepon', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'role': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'nomor_telepon': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded text-blue-600'}),
        }


# Form untuk Update (Edit) Informasi Profil Pengguna
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'nomor_telepon', 'alamat', 'is_active']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'role': forms.Select(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'nomor_telepon': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'alamat': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded text-blue-600'}),
        }
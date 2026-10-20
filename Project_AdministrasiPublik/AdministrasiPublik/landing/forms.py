from django import forms
from .models import Sambutan, Galeri, Berita, Akademik, TenagaPendidik
from django.core.exceptions import ValidationError
import re
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class SambutanForm(forms.ModelForm):
    class Meta:
        model = Sambutan
        fields = ['judul', 'nama_koor', 'isi_sambutan']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'nama_koor': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'isi_sambutan': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 5}),
        }

class GaleriForm(forms.ModelForm):
    class Meta:
        model = Galeri
        fields = ['judul', 'foto']

# Form Berita (Lengkap dengan CKEditor 5 dan Peringatan Slug Bahasa Indonesia)
class BeritaForm(forms.ModelForm):
    konten = forms.CharField(widget=CKEditor5Widget(config_name='extends'))

    class Meta:
        model = Berita
        fields = ['judul', 'slug', 'gambar', 'konten']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Masukkan judul berita...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50',
                'placeholder': 'otomatis-dari-judul-atau-isi-manual'
            }),
            'gambar': forms.ClearableFileInput(attrs={
                'class': 'w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100'
            }),
        }

    # Validasi custom agar pesan error slug menjadi Bahasa Indonesia
    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise ValidationError("Slug hanya boleh berisi huruf, angka, garis bawah (_), atau tanda hubung (-), serta TIDAK BOLEH menggunakan spasi atau huruf besar.")
        return slug

class TenagaPendidikForm(forms.ModelForm):
    class Meta:
        model = TenagaPendidik
        fields = ['nama', 'email', 'bidang_ilmu', 'nip', 'pangkat_gol', 'jabatan', 'foto']


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-white border border-slate-300 rounded-lg text-xs shadow-sm focus:outline-none focus:border-teal-600',
            'placeholder': 'Masukkan email Anda...'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-white border border-slate-300 rounded-lg text-xs shadow-sm focus:outline-none focus:border-teal-600',
            'placeholder': '••••••••'
        })
    )

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
        'placeholder': 'email atau username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
        'placeholder': '••••••••'
    }))

class AdminUserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Isi hanya jika ingin mengganti password baru'
        }), 
        required=False, 
        label="Password Baru"
    )
    
    class Meta:
        model = User
        # Tambahkan 'is_active' di sini
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'password']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password and password.strip():
            user.set_password(password)
            
        if commit:
            user.save()
        return user
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Isi hanya jika ingin mengganti password baru'
        }), 
        required=False, 
        label="Password Baru"
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'password']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        # Hanya ubah password jika kolomnya benar-benar diketik
        if password and password.strip():
            user.set_password(password)
            
        if commit:
            user.save()
        return user

# Form khusus Tambah User (Password Wajib)
class AdminUserCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Masukkan password untuk akun baru',
            'class': 'w-full px-3 py-2 border rounded-lg'
        }),
        required=True,
        label="Password"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


# Form khusus Edit User (Password Opsional - seperti yang tampil di screenshot lu)
class AdminUserUpdateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Isi hanya jika ingin mengganti password baru',
            'class': 'w-full px-3 py-2 border rounded-lg'
        }),
        required=False,
        label="Password Baru (Opsional)"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password and password.strip():
            user.set_password(password)
        if commit:
            user.save()
        return user
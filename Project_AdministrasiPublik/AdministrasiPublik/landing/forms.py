from django import forms
from .models import Sambutan, Galeri, Berita, Dosen, TenagaPendidik
from django.core.exceptions import ValidationError
import re
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.models import User, Group
from akun.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
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
        fields = ['nama', 'jk', 'kategori', 'status', 'pangkat', 'email', 'nip', 'nidn', 'telepon', 'foto']

class DosenForm(forms.ModelForm):
    class Meta:
        model = Dosen
        fields = [
            'nama', 'nip', 'nidn', 'nuptk', 'jenis_kelamin', 
            'bidang_ilmu', 'jabatan', 'pangkat_golongan', 
            'email', 'no_hp', 'status', 'foto'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'nip': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'nidn': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'nuptk': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs bg-white text-slate-800 focus:ring-2 focus:ring-teal-500'}),
            'bidang_ilmu': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'jabatan': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'pangkat_golongan': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs bg-white text-slate-800 focus:ring-2 focus:ring-teal-500'}),
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs bg-white text-slate-800 focus:ring-2 focus:ring-teal-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'no_hp': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500'}),
            'foto': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100'}),
        }


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


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Tambahkan styling Tailwind ke semua field form
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-800'
            })
            
        # Ubah label ke bahasa Indonesia
        self.fields['old_password'].label = 'Password Lama'
        self.fields['new_password1'].label = 'Password Baru'
        self.fields['new_password2'].label = 'Konfirmasi Password Baru'

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

# Pilihan Role
ROLE_CHOICES = [
    ('Super Admin', 'Super Admin'),
    ('Admin Prodi', 'Admin Prodi'),
    ('Editor', 'Editor'),
    ('Contributor', 'Contributor'),
]

class AdminUserCreateForm(forms.ModelForm):
    is_superuser = forms.BooleanField(
        required=False,
        label="Super Admin (Akses Penuh Sistem)",
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-teal-600 bg-white border-slate-300 rounded focus:ring-teal-500 cursor-pointer'
        })
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Role Tambahan (Grup)"
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full mt-1 px-3 py-2 text-xs bg-slate-50 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-600 focus:bg-white transition',
        'placeholder': '••••••••'
    }))
    
    is_active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-teal-600 bg-white border-slate-300 rounded focus:ring-teal-500 cursor-pointer'
        })
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'groups', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
        # Jika is_superuser dicentang, otomatis jadikan is_staff juga
        if self.cleaned_data.get('is_superuser'):
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = True
            
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['groups'])
        return user


class AdminUserUpdateForm(forms.ModelForm):
    is_superuser = forms.BooleanField(
        required=False,
        label="Super Admin (Akses Penuh Sistem)",
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-teal-600 bg-white border-slate-300 rounded focus:ring-teal-500 cursor-pointer'
        })
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Role Tambahan (Grup)"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'groups', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['is_superuser'].initial = self.instance.is_superuser

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if self.cleaned_data.get('is_superuser'):
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = True
            
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['groups'])
        return user
    
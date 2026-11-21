import os
from django import forms
from .models import (
    Sambutan, Galeri, Berita, Dosen, TenagaPendidik, TentangPage,
    VisiMisiTujuan, MisiItem, TujuanItem,
    AkademikPage, DokumenAkademik, Hero, EventTerdekat
)
from django.core.exceptions import ValidationError
import re
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.models import User, Group
from akun.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class TentangPageForm(forms.ModelForm):
    konten = forms.CharField(widget=CKEditor5Widget(config_name='extends'), required=False, label="Isi Konten")

    class Meta:
        model = TentangPage
        fields = ['judul', 'slug', 'file_dokumen', 'konten']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Masukkan nama sub-menu (misal: Profil Program Studi)'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50',
                'placeholder': 'misal: profil, sejarah, visi, dll'
            }),
            'file_dokumen': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none bg-white'
            }),
        }


class AkademikPageForm(forms.ModelForm):
    konten = forms.CharField(widget=CKEditor5Widget(config_name='extends'), required=False, label="Isi Konten")

    class Meta:
        model = AkademikPage
        fields = ['judul', 'slug', 'subjudul', 'urutan', 'link_eksternal', 'file_utama', 'konten', 'is_active']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Contoh: SIGA-8, Kurikulum, Jadwal Perkuliahan, dll.'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50',
                'placeholder': 'misal: siga-8, kurikulum, dll.'
            }),
            'subjudul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Keterangan singkat / subjudul'
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'min': 1
            }),
            'link_eksternal': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'https://siga.untad.ac.id (opsional)'
            }),
            'file_utama': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none bg-white'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500'
            }),
        }


class DokumenAkademikForm(forms.ModelForm):
    class Meta:
        model = DokumenAkademik
        fields = ['judul', 'file', 'keterangan']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Nama dokumen / lampiran berkas'
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none bg-white'
            }),
            'keterangan': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Keterangan berkas (opsional)'
            }),
        }


class VisiMisiTujuanForm(forms.ModelForm):
    class Meta:
        model = VisiMisiTujuan
        fields = ['visi', 'pengantar_misi', 'pengantar_tujuan']
        widgets = {
            'visi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs sm:text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none leading-relaxed',
                'rows': 4,
                'placeholder': 'Masukkan rumusan teks visi program studi...'
            }),
            'pengantar_misi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Contoh: Program Studi Administrasi Publik memiliki misi sebagai berikut:'
            }),
            'pengantar_tujuan': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Contoh: Program Studi Administrasi Publik memiliki tujuan Pendidikan berupa:'
            }),
        }


class MisiItemForm(forms.ModelForm):
    class Meta:
        model = MisiItem
        fields = ['urutan', 'deskripsi']
        widgets = {
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'min': 1
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs sm:text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none leading-relaxed',
                'rows': 3,
                'placeholder': 'Tuliskan poin misi program studi...'
            }),
        }


class TujuanItemForm(forms.ModelForm):
    class Meta:
        model = TujuanItem
        fields = ['urutan', 'judul', 'subjudul', 'deskripsi']
        widgets = {
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'min': 1
            }),
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Contoh: Employabilitas, Reputasi Akademik, dll.'
            }),
            'subjudul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none italic',
                'placeholder': 'Contoh: Employability (opsional)'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs sm:text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none leading-relaxed',
                'rows': 3,
                'placeholder': 'Tuliskan deskripsi lengkap dari tujuan program studi...'
            }),
        }




class SambutanForm(forms.ModelForm):
    class Meta:
        model = Sambutan
        fields = ['judul', 'nama_koor', 'isi_sambutan']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'nama_koor': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'isi_sambutan': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 5}),
        }


# (GaleriForm didefinisikan lengkap di bagian bawah)


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
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-slate-300 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-teal-500 text-slate-800'
            })
            
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
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_superuser', 'password']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
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
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser', 'groups', 'password', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        
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

class GaleriForm(forms.ModelForm):
    class Meta:
        model = Galeri
        fields = ['foto', 'urutan', 'judul']
        widgets = {
            'foto': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 text-xs border border-slate-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100',
                'accept': '.jpg,.jpeg,.png,.webp',
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Nomor urutan tampil (misal: 1, 2, 3...)',
                'min': 1
            }),
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Keterangan atau caption foto (opsional)'
            }),
        }

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto and hasattr(foto, 'size'):
            ext = os.path.splitext(foto.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                raise forms.ValidationError("Format foto tidak didukung! Hanya file .jpg, .jpeg, .png, dan .webp yang diperbolehkan.")
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Ukuran foto melebihi batas maksimal 5 MB.")
        return foto


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['video_file', 'video_url', 'foto', 'subjudul', 'judul', 'deskripsi']
        widgets = {
            'video_file': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 text-xs border border-slate-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100',
                'accept': '.mp4,.webm',
            }),
            'video_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Atau link video (misal: /static/video/banner.mp4 atau https://...)'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 text-xs border border-slate-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100',
                'accept': '.jpg,.jpeg,.png,.webp',
            }),
            'subjudul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Welcome to'
            }),
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Administrasi Publik'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none resize-none',
                'rows': 3,
                'placeholder': 'Fakultas Ilmu Sosial dan Ilmu Politik\nUniversitas Tadulako'
            }),
        }

    def clean_video_file(self):
        video = self.cleaned_data.get('video_file')
        if video and hasattr(video, 'size'):
            ext = os.path.splitext(video.name)[1].lower()
            if ext not in ['.mp4', '.webm']:
                raise forms.ValidationError("Format file video tidak didukung! Hanya file .mp4 dan .webm yang diperbolehkan.")
            if video.size > 100 * 1024 * 1024:
                raise forms.ValidationError(f"Ukuran video ({video.size / (1024*1024):.1f} MB) melebihi batas maksimal 100 MB.")
        return video

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if foto and hasattr(foto, 'size'):
            ext = os.path.splitext(foto.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                raise forms.ValidationError("Format gambar tidak didukung! Hanya file .jpg, .jpeg, .png, dan .webp yang diperbolehkan.")
            if foto.size > 5 * 1024 * 1024:
                raise forms.ValidationError(f"Ukuran gambar ({foto.size / (1024*1024):.1f} MB) melebihi batas maksimal 5 MB.")
        return foto


class EventTerdekatForm(forms.ModelForm):
    class Meta:
        model = EventTerdekat
        fields = [
            'nama_mahasiswa', 'nim', 'kategori', 'tanggal_event',
            'hari_tanggal_manual', 'waktu', 'lokasi', 'poster',
            'urutan', 'is_active'
        ]
        widgets = {
            'nama_mahasiswa': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Nama mahasiswa / peserta (misal: Ririn Puspita)',
                'required': True
            }),
            'nim': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'NIM (misal: G81122014) - opsional'
            }),
            'kategori': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Komprehensif, Seminar Proposal, Seminar Hasil, dll.',
                'required': True
            }),
            'tanggal_event': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'required': True
            }),
            'hari_tanggal_manual': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Opsional (misal: Rabu 24 Juni 2026)'
            }),
            'waktu': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Opsional (misal: 09:00 WITA - Selesai)'
            }),
            'lokasi': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'placeholder': 'Opsional (misal: Ruang Ujian Jurusan / Daring)'
            }),
            'poster': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 text-xs border border-slate-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none bg-slate-50 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100',
                'accept': '.jpg,.jpeg,.png,.webp'
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 border border-slate-300 rounded-xl text-xs focus:ring-2 focus:ring-teal-500 focus:outline-none',
                'min': 1
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500'
            }),
        }

    def clean_poster(self):
        poster = self.cleaned_data.get('poster')
        if poster and hasattr(poster, 'size'):
            ext = os.path.splitext(poster.name)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
                raise forms.ValidationError("Format flyer tidak didukung! Hanya file .jpg, .jpeg, .png, dan .webp yang diperbolehkan.")
            if poster.size > 5 * 1024 * 1024:
                raise forms.ValidationError(f"Ukuran file flyer ({poster.size / (1024*1024):.1f} MB) melebihi batas maksimal 5 MB.")
        return poster


from django import forms
from django.contrib.auth import get_user_model
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Berita, TenagaPendidik, PangkatGolongan, Sambutan
from .models import HalamanTentang, HalamanAkademik, DokumenAkademik

User = get_user_model()


# Form Berita (Field 'ringkasan' sudah dihapus)
class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'konten', 'gambar', 'posted_at']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Masukkan judul berita'
            }),
            'konten': forms.Textarea(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'rows': 5,
                'placeholder': 'Tulis isi artikel berita selengkapnya...'
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': 'image/*'
            }),
            'posted_at': forms.DateTimeInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'type': 'datetime-local'
            }),
        }


class TenagaPendidikForm(forms.ModelForm):
    pangkat_golongan = forms.ModelChoiceField(
        queryset=PangkatGolongan.objects.all().order_by('kategori', 'id'),
        required=False,
        empty_label="-- Pilih Pangkat / Golongan (PNS / PPPK) --",
        widget=forms.Select(attrs={
            'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs bg-slate-50 focus:bg-white'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'jenis' in self.fields:
            self.fields['jenis'].required = False
        for f in ['nidn', 'nip', 'nuptk', 'no_hp', 'email', 'foto', 'bidang_ilmu', 'status']:
            if f in self.fields:
                self.fields[f].required = False

    class Meta:
        model = TenagaPendidik
        fields = [
            'jenis', 'nama', 'jenis_kelamin', 'bidang_ilmu', 'status', 'foto',
            'email', 'nidn', 'nip', 'nuptk', 'no_hp', 'pangkat_golongan'
        ]
        widgets = {
            'jenis': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs font-semibold text-teal-800'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Nama lengkap & gelar'
            }),
            'jenis_kelamin': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs'
            }),
            'bidang_ilmu': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Bidang keilmuan / jabatan kerja'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': 'image/*'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'email@untad.ac.id'
            }),
            'nidn': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Nomor NIDN (opsional)'
            }),
            'nip': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Nomor NIP (opsional)'
            }),
            'nuptk': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Nomor NUPTK (opsional)'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': '0812xxxxxxxx'
            }),
        }


# Pilihan Role
ROLE_CHOICES = (
    ('Admin Prodi', 'Admin Prodi'),
    ('Editor', 'Editor'),
    ('Contributor', 'Contributor'),
)

# Form Tambah & Edit Pengguna (Manajemen User dengan Kotak Centang / Checkbox)
class UserForm(forms.ModelForm):
    role = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'w-4 h-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500'
        }),
        required=True,
        label="Role / Hak Akses"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
            'placeholder': 'Masukkan kata sandi'
        }),
        required=False,
        help_text="Wajib diisi saat membuat user baru. Kosongkan jika tidak ingin mengubah sandi saat edit."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Username akun'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'user@gmail.com'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and hasattr(self.instance, 'role') and self.instance.role:
            roles_aktif = [r.strip() for r in str(self.instance.role).split(',') if r.strip()]
            self.initial['role'] = roles_aktif

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.pk and not password:
            raise forms.ValidationError("Kata sandi wajib diisi untuk pengguna baru.")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        selected_roles = self.cleaned_data.get('role', [])
        user.role = ", ".join(selected_roles)

        role_str = user.role.lower()
        if 'admin' in role_str:
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user


# Form Khusus Sambutan (CKEditor 5)
class SambutanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['isi'].required = False

    class Meta:
        model = Sambutan
        fields = ['judul', 'nama_author', 'foto', 'isi']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Judul Sambutan'
            }),
            'nama_author': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Nama Koordinator Prodi'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': 'image/*'
            }),
            'isi': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, 
                config_name='extends'
            )
        }
        
class HalamanTentangForm(forms.ModelForm):
    class Meta:
        model = HalamanTentang
        fields = ['judul', 'isi']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs bg-slate-50 focus:bg-white focus:border-teal-700 outline-none transition',
                'placeholder': 'Masukkan judul halaman...'
            }),
        }

class HalamanAkademikForm(forms.ModelForm):
    class Meta:
        model = HalamanAkademik
        fields = ['judul', 'subjudul', 'link_eksternal', 'nama_file_utama', 'file_utama', 'isi']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs bg-slate-50 focus:bg-white focus:border-teal-700 outline-none transition',
                'placeholder': 'Masukkan judul halaman akademik...'
            }),
            'subjudul': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs bg-slate-50 focus:bg-white focus:border-teal-700 outline-none transition',
                'placeholder': 'Masukkan subjudul / deskripsi singkat...'
            }),
            'link_eksternal': forms.URLInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs bg-slate-50 focus:bg-white focus:border-teal-700 outline-none transition',
                'placeholder': 'https://siaga.untad.ac.id/ (opsional)'
            }),
            'nama_file_utama': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs bg-slate-50 focus:bg-white focus:border-teal-700 outline-none transition',
                'placeholder': 'Contoh: Unduh Kurikulum Lengkap (PDF)'
            }),
            'file_utama': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
            }),
            'isi': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, 
                config_name='extends'
            )
        }

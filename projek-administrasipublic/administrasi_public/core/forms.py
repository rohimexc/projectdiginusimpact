from django import forms
from django.contrib.auth import get_user_model
from .models import Berita, TenagaPendidik

User = get_user_model()


class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'ringkasan', 'konten', 'gambar', 'posted_at']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Masukkan judul berita'
            }),
            'ringkasan': forms.Textarea(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'rows': 2,
                'placeholder': 'Ringkasan singkat untuk kartu berita'
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
    class Meta:
        model = TenagaPendidik
        fields = [
            'jenis', 'nama', 'bidang_ilmu', 'status', 'foto',
            'email', 'nidn', 'nip', 'no_hp', 'pangkat_gol'
        ]
        widgets = {
            'jenis': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs font-semibold text-teal-800'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Nama lengkap & gelar'
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
                'placeholder': 'Nomor NIDN'
            }),
            'nip': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Nomor NIP'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': '0812xxxxxxxx'
            }),
            'pangkat_gol': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: Lektor Kepala / IV-a atau Pengadministrasi Umum'
            }),
        }


# Form Tambah & Edit Pengguna (Manajemen User)
class UserForm(forms.ModelForm):
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
        fields = ['username', 'email', 'role', 'is_active', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Username akun'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'user@gmail.com'
            }),
            # Menggunakan widget Select langsung dari pilihan model User
            'role': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs font-semibold'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 rounded border-slate-300 text-teal-600 focus:ring-teal-500'
            }),
        }

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

        # Otomatis atur status staff dan superuser jika rolenya admin
        role_str = str(user.role).strip().lower()
        if role_str == 'admin':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False

        if commit:
            user.save()
        return user
from django import forms
from django.contrib.auth import get_user_model
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Berita, TenagaPendidik, PangkatGolongan, Sambutan, Galeri, Hero, Event
from .models import HalamanTentang, HalamanAkademik, DokumenAkademik
from .validators import validate_image_file, validate_video_file, validate_document_file

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
                'accept': '.jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp',
                'data-upload-type': 'image',
                'data-max-mb': '10'
            }),
            'posted_at': forms.DateTimeInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'type': 'datetime-local'
            }),
        }

    def clean_gambar(self):
        file = self.cleaned_data.get('gambar')
        if file and hasattr(file, 'content_type'):
            validate_image_file(file)
        return file


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
        for f in ['nidn', 'nip', 'nuptk', 'no_hp', 'email', 'foto', 'bidang_ilmu', 'status', 'jabatan_fungsional']:
            if f in self.fields:
                self.fields[f].required = False

    class Meta:
        model = TenagaPendidik
        fields = [
            'jenis', 'nama', 'jenis_kelamin', 'jabatan_fungsional', 'bidang_ilmu', 'status', 'foto',
            'email', 'nidn', 'nip', 'nuptk', 'no_hp', 'pangkat_golongan'
        ]
        widgets = {
            'jenis': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs font-semibold text-teal-800'
            }),
            'jabatan_fungsional': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs'
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
                'accept': '.jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp',
                'data-upload-type': 'image',
                'data-max-mb': '10'
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

    def clean_foto(self):
        file = self.cleaned_data.get('foto')
        if file and hasattr(file, 'content_type'):
            validate_image_file(file)
        return file


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
                'accept': '.jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp',
                'data-upload-type': 'image',
                'data-max-mb': '10'
            }),
            'isi': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, 
                config_name='extends'
            )
        }

    def clean_foto(self):
        file = self.cleaned_data.get('foto')
        if file and hasattr(file, 'content_type'):
            validate_image_file(file)
        return file


class HalamanTentangForm(forms.ModelForm):
    class Meta:
        model = HalamanTentang
        fields = ['judul', 'gambar', 'isi']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-200 px-3.5 py-2.5 text-xs bg-slate-50 focus:bg-white focus:border-teal-700 outline-none transition',
                'placeholder': 'Masukkan judul halaman...'
            }),
            'gambar': forms.FileInput(attrs={
                'class': 'w-full p-2 border rounded-xl border-slate-200 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': '.jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp',
                'data-upload-type': 'image',
                'data-max-mb': '10'
            }),
            'isi': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, 
                config_name='extends'
            )
        }

    def clean_gambar(self):
        file = self.cleaned_data.get('gambar')
        if file and hasattr(file, 'content_type'):
            validate_image_file(file)
        return file


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
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx',
                'data-upload-type': 'document',
                'data-max-mb': '25'
            }),
            'isi': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, 
                config_name='extends'
            )
        }

    def clean_file_utama(self):
        file = self.cleaned_data.get('file_utama')
        if file and hasattr(file, 'content_type'):
            validate_document_file(file)
        return file


# Form Manajemen Galeri Foto
class GaleriForm(forms.ModelForm):
    class Meta:
        model = Galeri
        fields = ['gambar', 'urutan', 'judul']
        labels = {
            'gambar': 'Foto Galeri Kegiatan',
            'urutan': 'Urutan Tampilan',
            'judul': 'Judul / Keterangan Foto',
        }
        widgets = {
            'gambar': forms.FileInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': '.jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp',
                'data-upload-type': 'image',
                'data-max-mb': '10'
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: 1, 2, 3...',
                'min': '1',
            }),
            'judul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Masukkan judul atau keterangan kegiatan (opsional)'
            }),
        }

    def clean_gambar(self):
        file = self.cleaned_data.get('gambar')
        if file and hasattr(file, 'content_type'):
            validate_image_file(file)
        return file


# Form Manajemen Hero (1 Banner Tunggal: Link Video / Upload Video Maks 100MB & Gambar Hero)
class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['link_video', 'video_file', 'foto', 'judul', 'subjudul', 'deskripsi', 'is_active']
        labels = {
            'link_video': 'Link Video (YouTube atau URL MP4)',
            'video_file': 'Atau Upload Video (MP4/WEBM/OGG, Maksimal 100 MB)',
            'foto': 'Upload Gambar Hero (JPG/PNG/WEBP, Maks 10 MB)',
            'judul': 'Judul Utama Hero',
            'subjudul': 'Subjudul Hero',
            'deskripsi': 'Deskripsi Hero',
            'is_active': 'Aktifkan Tampilan Hero Kustom di Beranda',
        }
        widgets = {
            'link_video': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: https://www.youtube.com/watch?v=... atau https://domain.com/video.mp4'
            }),
            'video_file': forms.FileInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': '.mp4,.webm,.ogg,video/mp4,video/webm,video/ogg',
                'data-upload-type': 'video',
                'data-max-mb': '100'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': '.jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp',
                'data-upload-type': 'image',
                'data-max-mb': '10'
            }),
            'judul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: Program Studi Administrasi Publik'
            }),
            'subjudul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: Welcome to'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'rows': 3,
                'placeholder': 'Contoh: Fakultas Ilmu Sosial dan Ilmu Politik\nUniversitas Tadulako'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-brand-teal rounded border-slate-300 focus:ring-teal-500 cursor-pointer'
            }),
        }

    def clean_link_video(self):
        link = (self.cleaned_data.get('link_video') or '').strip()
        if link and not (link.startswith('http://') or link.startswith('https://')):
            raise forms.ValidationError('Link video harus diawali dengan http:// atau https://')
        return link

    def clean_video_file(self):
        file = self.cleaned_data.get('video_file')
        if file and hasattr(file, 'content_type'):
            validate_video_file(file)
        return file

    def clean_foto(self):
        file = self.cleaned_data.get('foto')
        if file and hasattr(file, 'content_type'):
            validate_image_file(file)
        return file


# ==========================================
# Form Manajemen Event / Agenda Terdekat (Rasio Poster 4:5)
# ==========================================
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'judul', 'kategori', 'poster', 'tanggal_mulai', 'tanggal_selesai',
            'waktu', 'lokasi', 'deskripsi', 'link_pendaftaran', 'is_active'
        ]
        labels = {
            'judul': 'Judul Event / Kegiatan',
            'kategori': 'Kategori Event',
            'poster': 'Poster Acara (Rasio 4:5)',
            'tanggal_mulai': 'Tanggal Mulai',
            'tanggal_selesai': 'Tanggal Selesai (Opsional)',
            'waktu': 'Waktu Pelaksanaan',
            'lokasi': 'Tempat / Lokasi Acara',
            'deskripsi': 'Deskripsi Lengkap Acara',
            'link_pendaftaran': 'Tautan Pendaftaran (Google Form / Link Eksternal)',
            'is_active': 'Tampilkan di Beranda (Status Aktif)',
        }
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs font-medium',
                'placeholder': 'Contoh: Seminar Nasional Tata Kelola Publik Digital'
            }),
            'kategori': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs font-semibold text-teal-800 bg-slate-50'
            }),
            'poster': forms.FileInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 bg-white text-xs file:mr-4 file:py-1.5 file:px-3.5 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': '.jpg,.jpeg,.png,.webp,image/jpeg,image/png,image/webp',
                'data-upload-type': 'image',
                'data-max-mb': '10'
            }),
            'tanggal_mulai': forms.DateInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'type': 'date'
            }),
            'tanggal_selesai': forms.DateInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'type': 'date'
            }),
            'waktu': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: 08.00 WITA - Selesai'
            }),
            'lokasi': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: Gedung Teater FISIP UNTAD / Zoom Cloud Meetings'
            }),
            'deskripsi': CKEditor5Widget(config_name='extends', attrs={'class': 'django_ckeditor_5'}),
            'link_pendaftaran': forms.URLInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-teal-500 text-xs',
                'placeholder': 'Contoh: https://bit.ly/daftar-seminar-ap'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-brand-teal rounded border-slate-300 focus:ring-teal-500 cursor-pointer'
            }),
        }

    def clean_poster(self):
        file = self.cleaned_data.get('poster')
        if file and hasattr(file, 'content_type'):
            validate_image_file(file)
        return file


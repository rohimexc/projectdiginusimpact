from django import forms
from .models import Sambutan, Galeri, Berita, Akademik, TenagaPendidik
from django.contrib.auth.forms import AuthenticationForm

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

class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'konten', 'gambar', 'post_date']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-lg'}),
            'konten': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-lg', 'rows': 6}),
            'post_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full p-2 border rounded-lg'}),
        }

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
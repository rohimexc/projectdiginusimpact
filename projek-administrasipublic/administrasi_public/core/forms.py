from django import forms
from .models import Berita, TenagaPendidik

class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'ringkasan', 'konten', 'gambar', 'posted_at']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Masukkan judul berita'
            }),
            'ringkasan': forms.Textarea(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300',
                'rows': 2,
                'placeholder': 'Ringkasan singkat untuk kartu berita'
            }),
            'konten': forms.Textarea(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300',
                'rows': 5,
                'placeholder': 'Tulis isi artikel berita selengkapnya...'
            }),
            # Menggunakan FileInput agar menjadi tombol upload berkas
            'gambar': forms.FileInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 bg-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': 'image/*'
            }),
            'posted_at': forms.DateTimeInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300',
                'type': 'datetime-local'
            }),
        }

class TenagaPendidikForm(forms.ModelForm):
    class Meta:
        model = TenagaPendidik
        fields = [
            'nama', 'bidang_ilmu', 'status', 'foto',
            'email', 'nidn', 'nip', 'no_hp', 'pangkat_gol'
        ]
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300', 'placeholder': 'Nama lengkap & gelar'}),
            'bidang_ilmu': forms.TextInput(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300', 'placeholder': 'Bidang keilmuan / kepakaran'}),
            'status': forms.Select(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300'}),
            # GANTI MENJADI FileInput AGAR MUNCUL TOMBOL CHOOSE FILE:
            'foto': forms.FileInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 bg-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-teal-50 file:text-brand-teal hover:file:bg-teal-100 cursor-pointer',
                'accept': 'image/*'
            }),
            'email': forms.EmailInput(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300', 'placeholder': 'email@untad.ac.id'}),
            'nidn': forms.TextInput(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300', 'placeholder': 'Nomor NIDN'}),
            'nip': forms.TextInput(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300', 'placeholder': 'Nomor NIP'}),
            'no_hp': forms.TextInput(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300', 'placeholder': '0812xxxxxxxx'}),
            'pangkat_gol': forms.TextInput(attrs={'class': 'w-full p-2.5 border rounded-xl border-slate-300', 'placeholder': 'Contoh: Lektor Kepala / IV-a'}),
        }
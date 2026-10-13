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
            'gambar': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300',
                'placeholder': 'URL gambar (misal: https://...)'
            }),
            'posted_at': forms.DateTimeInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300',
                'type': 'datetime-local'
            }),
        }

class TenagaPendidikForm(forms.ModelForm):
    class Meta:
        model = TenagaPendidik
        fields = ['nama', 'bidang_ilmu', 'status', 'foto', 'email', 'nidn', 'nip', 'no_hp', 'pangkat_gol']
        widgets = {
            'nama': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': 'Contoh: Dr. Ahmad Fauzi, M.Si'
            }),
            'bidang_ilmu': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': 'Contoh: Kebijakan Publik'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500'
            }),
            'foto': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': 'URL foto rasio 1:1'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': 'email@untad.ac.id'
            }),
            'nidn': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': 'Nomor NIDN'
            }),
            'nip': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': 'Nomor NIP'
            }),
            'no_hp': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': '0812xxxxxxx'
            }),
            'pangkat_gol': forms.TextInput(attrs={
                'class': 'w-full p-2.5 border rounded-xl border-slate-300 focus:ring-teal-500 focus:border-teal-500',
                'placeholder': 'Contoh: Lektor Kepala / IV-a'
            }),
        }
from django import forms
from .models import Berita

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
from django.contrib import admin
from .models import Sambutan, Galeri, Berita

# Mendaftarkan model ke halaman admin Django agar dapat dikelola melalui browser
admin.site.register(Sambutan)
admin.site.register(Galeri)
admin.site.register(Berita)
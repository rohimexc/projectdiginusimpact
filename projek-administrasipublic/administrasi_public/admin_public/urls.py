"""
URL configuration for admin_public project.
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Import view home, berita, dan tenaga pendidik dari core
from core.views import (
    home,
    berita_list,
    berita_detail,
    berita_create,
    berita_update,
    berita_delete,
    tenaga_pendidik_list,
    dosen_detail,
    dosen_create,
    dosen_update,
    dosen_delete,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Rute Berita
    path('Berita/', berita_list, name='berita_list'),
    path('Berita/tambah/', berita_create, name='berita_create'),
    path('Berita/<int:pk>/', berita_detail, name='berita_detail'),
    path('Berita/<int:pk>/edit/', berita_update, name='berita_update'),
    path('Berita/<int:pk>/hapus/', berita_delete, name='berita_delete'),

    # Rute Tenaga Pendidik / Staf Dosen
    path('tenaga-pendidik/', tenaga_pendidik_list, name='tenaga_pendidik_list'),
    path('tenaga-pendidik/<int:pk>/', dosen_detail, name='dosen_detail'),
    path('tenaga-pendidik/tambah/', dosen_create, name='dosen_create'),
    path('tenaga-pendidik/<int:pk>/edit/', dosen_update, name='dosen_update'),
    path('tenaga-pendidik/<int:pk>/hapus/', dosen_delete, name='dosen_delete'),

    # Jalur Media Langsung (Memaksa Django menyajikan gambar folder media)
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Konfigurasi Static Files
if settings.DEBUG:
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
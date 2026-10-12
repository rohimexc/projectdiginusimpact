"""
URL configuration for admin_public project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import view home dan seluruh view berita dari core
from core.views import (
    home,
    berita_list,
    berita_detail,
    berita_create,
    berita_update,
    berita_delete,
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
]

# Konfigurasi static dan media files saat mode development
if settings.DEBUG:
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    if hasattr(settings, 'MEDIA_ROOT') and settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
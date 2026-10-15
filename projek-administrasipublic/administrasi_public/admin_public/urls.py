"""
URL configuration for admin_public project.
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Import semua view dari core termasuk login & logout
from core.views import (
    home,
    berita_list,
    berita_detail,
    berita_create,
    berita_update,
    berita_delete,
    tenaga_kependidikan_list,
    tenaga_kependidikan_detail,
    tenaga_kependidikan_create,
    tenaga_kependidikan_update,
    tenaga_kependidikan_delete,
    user_login,
    user_logout,
)

urlpatterns = [
    # Rute logout admin diarahkan langsung ke halaman login sebelum rute bawaan admin
    path('admin/logout/', user_logout, name='admin_logout'),
    path('logout/', user_logout, name='user_logout'),
    path('login/', user_login, name='user_login'),

    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Rute Berita
    path('Berita/', berita_list, name='berita_list'),
    path('Berita/tambah/', berita_create, name='berita_create'),
    path('Berita/<int:pk>/', berita_detail, name='berita_detail'),
    path('Berita/<int:pk>/edit/', berita_update, name='berita_update'),
    path('Berita/<int:pk>/hapus/', berita_delete, name='berita_delete'),

    # Rute Tenaga Kependidikan
    path('tenaga-kependidikan/', tenaga_kependidikan_list, name='tenaga_kependidikan_list'),
    path('tenaga-kependidikan/<int:pk>/', tenaga_kependidikan_detail, name='tenaga_kependidikan_detail'),
    path('tenaga-kependidikan/tambah/', tenaga_kependidikan_create, name='tenaga_kependidikan_create'),
    path('tenaga-kependidikan/<int:pk>/edit/', tenaga_kependidikan_update, name='tenaga_kependidikan_update'),
    path('tenaga-kependidikan/<int:pk>/hapus/', tenaga_kependidikan_delete, name='tenaga_kependidikan_delete'),

    # Jalur Media Upload
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# Konfigurasi Static Files
if settings.DEBUG:
    if hasattr(settings, 'STATICFILES_DIRS') and settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    else:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
URL configuration for admin_public project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Mengimpor modul panel admin bawaan Django
from django.contrib import admin

# Mengimpor fungsi path untuk memetakan rute URL ke fungsi view
from django.urls import path

# Mengimpor fungsi view 'home' yang sudah dibuat di file core/views.py
from core.views import home

from django.conf.urls.static import static
from django.conf import settings
# Daftar pola rute URL yang bisa diakses di website
urlpatterns = [
    # Rute untuk mengakses dashboard/panel admin Django (contoh: 127.0.0.1:8000/admin/)
    path('admin/', admin.site.urls),
    
    # Rute halaman utama/root URL (127.0.0.1:8000/) yang akan menjalankan fungsi 'home'
    path('', home, name='home'),
]

if settings.DEBUG:

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
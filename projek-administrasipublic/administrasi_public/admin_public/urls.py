"""
URL configuration for admin_public project.
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Import view dari core
from core.views import (
    home,
    berita_list,
    berita_detail,
    berita_create,
    berita_update,
    berita_delete,
    tenaga_pendidik_list,
    tenaga_kependidikan_list,
    tenaga_kependidikan_detail,
    tenaga_kependidikan_create,
    tenaga_kependidikan_update,
    tenaga_kependidikan_delete,
    # View CRUD Dosen & Tendik
    dosen_create,
    dosen_update,
    dosen_delete,
    tendik_create,
    tendik_update,
    tendik_delete,
    user_login,
    user_logout,
    admin_dashboard,
    admin_kelola_sambutan,
    admin_kelola_berita,
    admin_kelola_dosen,
    admin_kelola_tendik,
    admin_kelola_user,
    user_toggle_status,
    user_create,
    user_update,
    user_delete,
    # View Kelola Halaman Tentang
    admin_kelola_tentang,
    tentang_detail,
)

urlpatterns = [
    # Route Wajib CKEditor 5 (Penyelesai Error ck_editor_5_upload_file)
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # Rute Logout & Login
    path('admin/logout/', user_logout, name='admin_logout'),
    path('logout/', user_logout, name='user_logout'),
    path('login/', user_login, name='user_login'),

    # Alur Reset Password via Email
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='core/auth/password_reset.html',
             email_template_name='core/auth/password_reset_email.html',
             subject_template_name='core/auth/password_reset_subject.txt',
             success_url='/password-reset/done/'
         ), 
         name='password_reset'),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='core/auth/password_reset_done.html'
         ), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='core/auth/password_reset_confirm.html',
             success_url='/password-reset-complete/'
         ), 
         name='password_reset_confirm'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='core/auth/password_reset_complete.html'
         ), 
         name='password_reset_complete'),

    # Rute Dashboard Admin & Sambutan
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/sambutan/', admin_kelola_sambutan, name='admin_kelola_sambutan'),
    path('dashboard/berita/', admin_kelola_berita, name='admin_kelola_berita'),
    
    # Rute Kelola Halaman Tentang (Profil, Visi Misi, Tujuan, dll)
    path('dashboard/tentang/<str:kategori>/', admin_kelola_tentang, name='admin_kelola_tentang'),
    path('tentang/<str:kategori>/', tentang_detail, name='tentang_detail'),
    
    # Rute Dosen Admin
    path('dashboard/dosen/', admin_kelola_dosen, name='admin_kelola_dosen'),
    path('dashboard/dosen/tambah/', dosen_create, name='dosen_create'),
    path('dashboard/dosen/<int:pk>/edit/', dosen_update, name='dosen_update'),
    path('dashboard/dosen/<int:pk>/hapus/', dosen_delete, name='dosen_delete'),

    # Rute Tendik Admin
    path('dashboard/tendik/', admin_kelola_tendik, name='admin_kelola_tendik'),
    path('dashboard/tendik/tambah/', tendik_create, name='tendik_create'),
    path('dashboard/tendik/<int:pk>/edit/', tendik_update, name='tendik_update'),
    path('dashboard/tendik/<int:pk>/hapus/', tendik_delete, name='tendik_delete'),

    # Rute CRUD Manajemen User
    path('dashboard/users/', admin_kelola_user, name='admin_kelola_user'),
    path('dashboard/users/tambah/', user_create, name='user_create'),
    path('dashboard/users/<int:pk>/edit/', user_update, name='user_update'),
    path('dashboard/users/<int:pk>/hapus/', user_delete, name='user_delete'),
    path('dashboard/users/<int:pk>/toggle/', user_toggle_status, name='user_toggle_status'),

    # Django Admin Bawaan & Beranda Publik
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    # Rute Berita
    path('Berita/', berita_list, name='berita_list'),
    path('Berita/tambah/', berita_create, name='berita_create'),
    path('Berita/<int:pk>/', berita_detail, name='berita_detail'),
    path('Berita/<int:pk>/edit/', berita_update, name='berita_update'),
    path('Berita/<int:pk>/hapus/', berita_delete, name='berita_delete'),

    # Rute Publik Tenaga Pendidik & Kependidikan
    path('tenaga-pendidik/', tenaga_pendidik_list, name='tenaga_pendidik_list'),
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
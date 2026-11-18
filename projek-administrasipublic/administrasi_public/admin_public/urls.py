from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Import view dari core.views
from core.views import (
    home,
    galeri_list,
    berita_list,
    berita_detail,
    berita_like,
    berita_share,
    komentar_edit,
    komentar_hapus,
    berita_create,
    berita_update,
    berita_delete,
    tenaga_pendidik_list,
    tenaga_kependidikan_list,
    tenaga_kependidikan_detail,
    tenaga_kependidikan_create,
    tenaga_kependidikan_update,
    tenaga_kependidikan_delete,
    dosen_create,
    dosen_update,
    dosen_delete,
    tendik_create,
    tendik_update,
    tendik_delete,
    user_register,
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
    admin_kelola_tentang,
    tentang_detail,
    admin_kelola_visi_misi,
    akademik_detail,
    admin_kelola_akademik,
    admin_hapus_dokumen_akademik,
    admin_kelola_galeri,
    galeri_create,
    galeri_update,
    galeri_delete,
    admin_kelola_hero,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor5/', include('django_ckeditor_5.urls')),

    # 1. Halaman Publik Utama
    path('', home, name='home'),
    path('galeri/', galeri_list, name='galeri_list'),
    path('Berita/', berita_list, name='berita_list'),
    path('Berita/<int:pk>/', berita_detail, name='berita_detail'),
    path('Berita/<int:pk>/like/', berita_like, name='berita_like'),
    path('Berita/<int:pk>/share/', berita_share, name='berita_share'),

    # 2. Aksi AJAX Komentar
    path('komentar/<int:pk>/edit/', komentar_edit, name='komentar_edit'),
    path('komentar/<int:pk>/hapus/', komentar_hapus, name='komentar_hapus'),

    # 3. Publik Staf, Tentang & Akademik
    path('staf/tenaga-pengajar/', tenaga_pendidik_list, name='tenaga_pendidik_list'),
    path('staf/tenaga-kependidikan/', tenaga_kependidikan_list, name='tenaga_kependidikan_list'),
    path('staf/tenaga-kependidikan/<int:pk>/', tenaga_kependidikan_detail, name='tenaga_kependidikan_detail'),
    path('tentang/<str:kategori>/', tentang_detail, name='tentang_detail'),
    path('akademik/<str:kategori>/', akademik_detail, name='akademik_detail'),

    # 4. Auth
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),

    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='core/auth/password_reset.html',
        email_template_name='core/auth/password_reset_email.html',
        subject_template_name='core/auth/password_reset_subject.txt',
        success_url='/password-reset/done/'
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/auth/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/auth/password_reset_confirm.html',
        success_url='/password-reset-complete/'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/auth/password_reset_complete.html'
    ), name='password_reset_complete'),

    # 5. Dashboard Admin
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/sambutan/', admin_kelola_sambutan, name='admin_kelola_sambutan'),
    path('dashboard/visi-misi/', admin_kelola_visi_misi, name='admin_kelola_visi_misi'),
    path('dashboard/tentang/<str:kategori>/', admin_kelola_tentang, name='admin_kelola_tentang'),
    path('dashboard/akademik/', admin_kelola_akademik, name='admin_kelola_akademik'),
    path('dashboard/akademik/<str:kategori>/', admin_kelola_akademik, name='admin_kelola_akademik_kategori'),
    path('dashboard/akademik/hapus-dokumen/<int:pk>/', admin_hapus_dokumen_akademik, name='admin_hapus_dokumen_akademik'),

    # 6. Admin Kelola Data
    path('dashboard/berita/', admin_kelola_berita, name='admin_kelola_berita'),
    path('dashboard/berita/tambah/', berita_create, name='berita_create'),
    path('dashboard/berita/edit/<int:pk>/', berita_update, name='berita_update'),
    path('dashboard/berita/hapus/<int:pk>/', berita_delete, name='berita_delete'),

    path('dashboard/dosen/', admin_kelola_dosen, name='admin_kelola_dosen'),
    path('dashboard/dosen/tambah/', dosen_create, name='dosen_create'),
    path('dashboard/dosen/edit/<int:pk>/', dosen_update, name='dosen_update'),
    path('dashboard/dosen/hapus/<int:pk>/', dosen_delete, name='dosen_delete'),

    path('dashboard/tendik/', admin_kelola_tendik, name='admin_kelola_tendik'),
    path('dashboard/tendik/tambah/', tendik_create, name='tendik_create'),
    path('dashboard/tendik/edit/<int:pk>/', tendik_update, name='tendik_update'),
    path('dashboard/tendik/hapus/<int:pk>/', tendik_delete, name='tendik_delete'),

    path('dashboard/user/', admin_kelola_user, name='admin_kelola_user'),
    path('dashboard/user/tambah/', user_create, name='user_create'),
    path('dashboard/user/edit/<int:pk>/', user_update, name='user_update'),
    path('dashboard/user/hapus/<int:pk>/', user_delete, name='user_delete'),
    path('dashboard/user/toggle/<int:pk>/', user_toggle_status, name='user_toggle_status'),

    # 7. Admin Kelola Hero (Tunggal)
    path('dashboard/hero/', admin_kelola_hero, name='admin_kelola_hero'),

    # 8. Admin Kelola Galeri (Foto & Urutan)
    path('dashboard/galeri/', admin_kelola_galeri, name='admin_kelola_galeri'),
    path('dashboard/galeri/tambah/', galeri_create, name='galeri_create'),
    path('dashboard/galeri/edit/<int:pk>/', galeri_update, name='galeri_update'),
    path('dashboard/galeri/hapus/<int:pk>/', galeri_delete, name='galeri_delete'),
]

# Static & Media URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path, include
from . import views
from akun.views import manajemen_user_view, audit_log_view
from django.contrib.auth import views as auth_views

app_name = 'landing'
urlpatterns = [
    path('', views.index, name='landing_home'),
    path('berita/', views.berita_list_view, name='berita_list'),
    path('berita/tambah/', views.berita_create_view, name='berita_create'),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('berita/<slug:slug>/', views.berita_detail_view, name='berita_detail'),
    path('berita/<slug:slug>/edit/', views.berita_update_view, name='berita_update'),
    path('berita/<slug:slug>/hapus/', views.berita_delete_view, name='berita_delete'),
    
    path('tenaga-pendidik/', views.tenaga_pendidik_beranda_view, name='tenaga_pendidik_beranda'),
    path('dashboard/tendik/', views.tenaga_pendidik_view, name='tenaga_pendidik'),
    path('dashboard/tendik/tambah/', views.tendik_create_view, name='tendik_create'),
    path('dashboard/tendik/<int:pk>/ubah/', views.tendik_update_view, name='tendik_update'),
    path('dashboard/tendik/<int:pk>/hapus/', views.tendik_delete_view, name='tendik_delete'),
    
    # --- URL HALAMAN LOGIN & ADMIN ---
    path('login/', views.login_view, name='login'),
    path('dashboard-admin/', views.dashboard_admin_khusus, name='dashboard_admin'),
    path('dashboard/berita/', views.dashboard_berita_view, name='dashboard_berita'),
    
    # Rute Manajemen User & Audit Log
    path('dashboard/manajemen-user/', manajemen_user_view, name='manajemen_user'),
    path('dashboard/audit-log/', audit_log_view, name='audit_log'),
    path('admin-portal/user/tambah/', views.user_create_view, name='user_create'),
    path('admin-portal/user/edit/<int:pk>/', views.user_update_view, name='user_update'),
    path('admin-portal/user/hapus/<int:pk>/', views.user_delete_view, name='user_delete'),

# --- URL PASSWORD RESET ---
path('admin-portal/password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='landing/user/password_reset_form.html',
             email_template_name='landing/user/password_reset_email.html', # <--- INI KUNCINYA
             success_url='/admin-portal/password-reset/done/'
         ), 
         name='password_reset'),
    
    path('admin-portal/password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='landing/user/password_reset_done.html'
         ), 
         name='password_reset_done'),
    
    path('admin-portal/reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='landing/user/password_reset_confirm.html',
             success_url='/admin-portal/reset/done/'
         ), 
         name='password_reset_confirm'),
    
    path('admin-portal/reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='landing/user/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
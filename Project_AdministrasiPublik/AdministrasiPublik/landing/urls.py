from django.urls import path
from . import views

app_name = 'landing'
urlpatterns = [
    path('', views.index , name='landing_home'),
    path('berita/', views.berita_list_view, name='berita_list'),
    path('berita/tambah/', views.berita_create_view, name='berita_create'),
    path('berita/<slug:slug>/', views.berita_detail_view, name='berita_detail'),
    path('berita/<slug:slug>/edit/', views.berita_update_view, name='berita_update'),
    path('berita/<slug:slug>/hapus/', views.berita_delete_view, name='berita_delete'),
path('tenaga-pendidik/', views.tenaga_pendidik_beranda_view, name='tenaga_pendidik_beranda'), # Buat umum/publik
path('dashboard/tendik/', views.tenaga_pendidik_view, name='tenaga_pendidik'),
path('dashboard/tendik/tambah/', views.tendik_create_view, name='tendik_create'),
path('dashboard/tendik/<int:pk>/ubah/', views.tendik_update_view, name='tendik_update'),
path('dashboard/tendik/<int:pk>/hapus/', views.tendik_delete_view, name='tendik_delete'),
    # --- URL HALAMAN LOGIN ---
    path('login/', views.login_view, name='login'),
    path('dashboard-admin/', views.dashboard_admin_khusus, name='dashboard_admin'),
    path('dashboard/berita/', views.dashboard_berita_view, name='dashboard_berita'),
]
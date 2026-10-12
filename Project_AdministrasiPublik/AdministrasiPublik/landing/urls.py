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
]
from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # Halaman Publik Dinamis
    path('p/<slug:slug>/', views.page_detail, name='page_detail'),

    # Admin Dashboard - Manajemen Menu Navigasi
    path('admin-portal/cms/menus/', views.dashboard_menu_list, name='dashboard_menu_list'),
    path('admin-portal/cms/menus/tambah/', views.dashboard_menu_create, name='dashboard_menu_create'),
    path('admin-portal/cms/menus/<int:pk>/edit/', views.dashboard_menu_edit, name='dashboard_menu_edit'),
    path('admin-portal/cms/menus/<int:pk>/hapus/', views.dashboard_menu_delete, name='dashboard_menu_delete'),
    path('admin-portal/cms/menus/reorder/', views.dashboard_menu_reorder, name='dashboard_menu_reorder'),

    # Admin Dashboard - Manajemen Halaman (Pages)
    path('admin-portal/cms/pages/', views.dashboard_page_list, name='dashboard_page_list'),
    path('admin-portal/cms/pages/tambah/', views.dashboard_page_create, name='dashboard_page_create'),
    path('admin-portal/cms/pages/<int:pk>/edit/', views.dashboard_page_edit, name='dashboard_page_edit'),
    path('admin-portal/cms/pages/<int:pk>/hapus/', views.dashboard_page_delete, name='dashboard_page_delete'),

    # Admin Dashboard - Pengaturan Situs (Site Settings)
    path('admin-portal/cms/site-settings/', views.dashboard_site_settings, name='dashboard_site_settings'),
    path('admin-portal/cms/social/tambah/', views.dashboard_social_create, name='dashboard_social_create'),
    path('admin-portal/cms/social/<int:pk>/hapus/', views.dashboard_social_delete, name='dashboard_social_delete'),
    path('admin-portal/cms/quicklink/tambah/', views.dashboard_quicklink_create, name='dashboard_quicklink_create'),
    path('admin-portal/cms/quicklink/<int:pk>/hapus/', views.dashboard_quicklink_delete, name='dashboard_quicklink_delete'),
]

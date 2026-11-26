from django.urls import path
from .views import page_detail, reorder_menus

urlpatterns = [
    # Dynamic Page Routing by Slug
    path('page/<slug:slug>/', page_detail, name='cms_page_detail'),
    # API Drag & Drop Reordering
    path('cms/api/reorder-menus/', reorder_menus, name='cms_reorder_menus'),
]

from django.urls import path

from . import views


urlpatterns = [
    path('cari/', views.cari),
    path('',views.index),
]
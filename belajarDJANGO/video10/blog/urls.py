from django.urls import path

from . import views


urlpatterns = [
    path('Artikel/', views.Artikel),
    path('Berita/', views.Berita),
    path('',views.index),
]
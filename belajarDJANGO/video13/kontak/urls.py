from django.urls import path
from . import views

appname = 'kontak'
urlpatterns = [
    path('',views.index),
]

from django.contrib import admin
from django.urls import path , include


# pola 1
#from .views import index, blog
#pola 2 
from . import views
#pola 3
#from . views import *
from kontak import views as kontakviews

urlpatterns = [
    path('blog/', include('blog.urls')),
    path('kontak/', kontakviews.index,),
    path('', views.index),
    path('admin/', admin.site.urls),
]

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'blog.html')

def cari(request):
    return HttpResponse("Hello, world. You're at the blog cari.")
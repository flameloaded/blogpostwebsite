from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'bloghomepage/home.html')

def about(request):
    return render(request, 'bloghomepage/about.html')
# Create your views here.

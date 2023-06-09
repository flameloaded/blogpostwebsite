from django.shortcuts import render
from .models import Post
# from django.http import HttpResponse

"""posts = [
    { 
        'title' : 'first post',
        'content': 'this is my first content post',
        'author': 'david okon',
        'date_posted': '12, May, 2023'

    },
    {
        'title': 'second post',
        'content': 'this is my second post',
        'author': 'samuel okon',
        'date_posted': '12, May, 2023'
    }

]"""

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'bloghomepage/home.html', context)

def about(request):
    return render(request, 'bloghomepage/about.html')
# Create your views here.

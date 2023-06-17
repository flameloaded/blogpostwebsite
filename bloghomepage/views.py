from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

"""def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'bloghomepage/home.html', context)"""

def about(request):
    return render(request, 'bloghomepage/about.html')
# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'bloghomepage/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.content = post.content[:100] + '...'  # Truncate the content
        return context

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'bloghomepage/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 4
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for post in context['posts']:
            post.content = post.content[:100] + '...'  # Truncate the content
        return context

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post

class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    success_message = 'post was created successfully'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


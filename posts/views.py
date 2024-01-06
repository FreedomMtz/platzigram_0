"""Posts views."""

# Django 
from django.contrib.auth.decorators import login_required # Decorador para mostrar contenido si estamos logeados.
from django.shortcuts import render, redirect #Ahora si utilizaremos render
from django.contrib.auth.mixins import LoginRequiredMixin # Modulo para asefurar las classes de vistas.
from django.views.generic import CreateView, DetailView, ListView # Se utiliza para crear vistas que rendericen una lista de objetos desde una base de datos, como por ejemplo, mostrar una lista de usuarios, publicaciones de un blog
from django.urls import reverse_lazy

# Forms
from posts.forms import PostForm
from posts.models import Post

# Create your views here.

class PostsFeedView(LoginRequiredMixin, ListView):  # Clase para la paginacion.
    """Return all published posts."""
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 20
    context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    """Return detail posts."""
    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'
    
class CreatePostView(LoginRequiredMixin,CreateView):
    """Create a new post."""
    template_name= 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')
    
    def get_context_data(self, **kwargs):
        """Add user and profile to context."""
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        return context
    
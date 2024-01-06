"""Users views."""
# Django.
from typing import Any
from django.contrib.auth import authenticate, login, logout # Importamos las librerias para un ingreso correcto.
from django.contrib.auth.decorators import login_required # Importamos al decorador "login_r.."para evitar logout repentino.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views #Importamos una vista generica para utulizar "Authenticate"
from django.db.models.base import Model as Model
from django.shortcuts import render, redirect # Redirect solo acepta valores ".html" o sus "names".
from django.views.generic import DetailView, FormView, UpdateView # Modulo para crear clases de view.
from django.urls import reverse, reverse_lazy # Modulo para crear URLS.


# Forms
from users.forms import SignupForm

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile


# Create your views here.
"""
#Solucion propia
class PostDetailView(LoginRequiredMixin, DetailView):
    
    template_name = 'posts/detail.html'
    slug_field = 'id' # Actua como una PK ya que no hay usuarios repetidos.
    slug_url_kwarg = 'id' # Es el valor que se le agergará en cada campo al buscar un perfil.
    queryset = Post.objects.all() # Aqui importamos todos los datos de usuairos y procesarlos segun la accion.
    context_object_name = 'post' # Este será el nombre del objeto que manejaremos en las templates.

     def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['posts'] = Post.objects.filter(id=post.id)
        return context  """
    
class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view. Independientemente si es propio o de otro usuario
    se crea una clase ya que la logica que se va a utilizar es un poco mas robusta."""
    login_url = 'users:login' # En dado caso de que ingresemos sin usuario nos redireccionará.
    template_name = 'users/detail.html'
    slug_field = 'username' # Acrua como una PK ya que no hay usuarios repetidos.
    slug_url_kwarg = 'username' # Es el valor que se le agergará en cada campo al buscar un perfil.
    queryset = User.objects.all() # Aqui importamos todos los datos de usuairos y procesarlos segun la accion.
    context_object_name = 'user' # Este será el nombre del objeto que manejaremos en las templates.

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context 
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""
    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']
    
    def get_object(self):
        """Regresamos el usuario del Perfil actual, esto para armar una "URL compuesta"."""
        return self.request.user.profile
    
    def get_success_url(self):
        """Creamos la "URL" con el nombre de usuario obtenido en la  linea anterior."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})
    


class SignUpView(auth_views.LoginView, FormView):
    """Users sign up. Utilizando "FromView" """
    
    """Signup a user."""
    """ login_url = '/' #En realidad solo úede funcionar con redirect_field_name"""
    redirect_field_name = 'posts:feed'
    redirect_authenticated_user = True
    
    
    
    template_name = "users/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

class LoginView(auth_views.LoginView):
    """Login view."""
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout view."""
    template_name = 'users/logged_out.html' #Esta direccion no será requerida para el proceso pero si para declarar la funcion.
     
        
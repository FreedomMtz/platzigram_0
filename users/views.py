"""Users views."""
# Django.
from typing import Any
from django.contrib.auth import authenticate, login, logout # Importamos las librerias para un ingreso correcto.
from django.contrib.auth.decorators import login_required # Importamos al decorador "login_r.."para evitar logout repentino.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views #Importamos una vista generica para utulizar "Authenticate"
from django.contrib import messages
from django.test import override_settings
from django.db.models.base import Model as Model
from django.shortcuts import render, redirect, get_object_or_404 # Redirect solo acepta valores ".html" o sus "names".
from django.views.generic import DetailView, FormView, UpdateView, DeleteView # Modulo para crear clases de view.
from django.urls import reverse, reverse_lazy # Modulo para crear URLS.
from django.http import HttpResponseRedirect


# Forms
from users.forms import SignupForm

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile, Follow


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
    slug_field = 'username' # Actua como una PK ya que no hay usuarios repetidos.
    slug_url_kwarg = 'username' # Es el valor que se le agergará en cada campo al buscar un perfil.
    queryset = User.objects.all() # Aqui importamos todos los datos de usuairos y procesarlos segun la accion.
    context_object_name = 'user' # Este será el nombre del objeto que manejaremos en las templates.

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        follower=self.request.user  #Corresponde al following_update 
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        context['posts_count'] = Post.objects.filter(user=user).count()
        context['following_count'] = Follow.objects.filter(follower=user).count()
        context['followers_count'] = Follow.objects.filter(following=user).count()
        context['following_update'] = Follow.objects.filter(follower= follower, following=user).count()

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
 
@login_required
#@override_settings(MIDDLEWARE=['platzigram.middleware.ProfileCompletionMiddlewere'])
def delete_user(request):
    user = request.user
    print("eliminacion de perfil1")
    if request.method == 'POST':
        # Eliminar el usuario y cerrar la sesión
        print("eliminacion de perfil2")
        user.delete()
        logout(request)
        #messages.success(request, 'Tu cuenta ha sido eliminada exitosamente.')
        return redirect('users:login')  # Reemplaza con tu URL de inicio
    return render(request, 'users/delete_user.html')
 
@login_required
def delete_picture(request):
    user = request.user
    #print("bander111")
    if request.method == "POST":
        #print("bander1")
        if user.profile.picture:
            user.profile.picture.delete()
            #print("bander2")
        return redirect("users:update")
    #print("bander3")

    return render(request, 'users/delete_picture.html')
   
class SignUpView(FormView):
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

@login_required
def FollowView(request, username):
    user = request.user #Usuario logeado
    following = get_object_or_404(User, username=username) #Traemos al modelo user del usuario visitado
    follow = Follow.objects.filter(follower=user, following=following).count()
    if not follow:
        follow = Follow.objects.create(follower=user, following=following)
        follow.save()
    else:
        follow = Follow.objects.filter(follower=user, following=following).delete()
        
    
    return  HttpResponseRedirect(reverse('users:detail', args=[username]))

""" #def FollowersView(request, username):

    ###user_loged = request.user #Usuario logeado actualmente
    #user = get_object_or_404(User, username=username) #Usuario del perfil que estamos viendo
    #followers_filter_names = Follow.objects.filter(following=user) #Filtramos para buscar quienes siguen a nuestro usuario actual
    #followers_names = [names.follower.username for names in followers_filter_names]
    #followers_names = sorted(followers_names)
    ###print(followers_names)

    #########
    #context = {
    #    'followers_names': followers_names,
    #    'user': user
    #}
    #return render(request, 'users/followers.html',  context) """

class FollowerView(LoginRequiredMixin, DetailView):
    """User detail view. Independientemente si es propio o de otro usuario
    se crea una clase ya que la logica que se va a utilizar es un poco mas robusta."""
    login_url = 'users:login' # En dado caso de que ingresemos sin usuario nos redireccionará.
    template_name = 'users/followers.html'
    slug_field = 'username' # Actua como una PK ya que no hay usuarios repetidos.
    slug_url_kwarg = 'username' # Es el valor que se le agergará en cada campo al buscar un perfil.
    queryset = User.objects.all() # Aqui importamos todos los datos de usuairos y procesarlos segun la accion.
    context_object_name = 'user' # Este será el nombre del objeto que manejaremos en las templates.

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        followers_filter_names = Follow.objects.filter(following=user) #Filtramos para buscar quienes siguen a nuestro usuario actual
        followers_names = [names.follower.username for names in followers_filter_names]
        followers_names = sorted(followers_names)
        
        users_filter = User.objects.filter(username__in=followers_names) #Obtenemos los modelos con la lista obtenida anteriormente.
       
        context['users_filter'] = users_filter

        return context 


class FollowingView(LoginRequiredMixin, DetailView): #Clase de la view Following
    login_url='users:login'
    template_name = 'users/following.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        following_filter_names = Follow.objects.filter(follower=user) #Filtramos para buscar quienes siguen a nuestro usuario actual
        following_names = [names.following.username for names in following_filter_names] #Obtenemos una lista de nombres
        following_names = sorted(following_names) #Ordenamos los datos
        
        users_filter = User.objects.filter(username__in=following_names) #Obtenemos los modelos con la lista obtenida anteriormente.
        
        #print(users_filter)
        #print(type(users_filter))
        #print("*****************")
        #print(user)
        #print(type(user))
        
        context['users_filter'] = users_filter
        
        return context
    
    
""" def FollowingView(request, username):
    user = get_object_or_404(User, username=username) #Usuario del perfil que estamos viendo
    following_filter_names = Follow.objects.filter(follower=user) #Filtramos para buscar quienes siguen a nuestro usuario actual
    following_names = [names.following.username for names in following_filter_names]
    following_names = sorted(following_names)
    print(following_names)
    
    #########
    context = {
        'following_names': following_names,
        'user': user
    }
    return render(request, 'users/following.html',  context) """
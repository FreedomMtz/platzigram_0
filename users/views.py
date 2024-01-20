"""Users views."""
# Django.
from typing import Any
# Importamos las librerias para un ingreso correcto.
from django.contrib.auth import logout
# Importamos al decorador "login_r.."para evitar logout repentino.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Importamos una vista generica para utulizar "Authenticate"
from django.contrib.auth import views as auth_views
from django.db.models.base import Model as Model
# Redirect solo acepta valores ".html" o sus "names".
from django.shortcuts import render, redirect, get_object_or_404
# Modulo para crear clases de view.
from django.views.generic import DetailView, FormView, UpdateView
from django.urls import reverse, reverse_lazy  # Modulo para crear URLS.
from django.http import HttpResponseRedirect

# Forms
from users.forms import SignupForm

# Models
from django.contrib.auth.models import User
from posts.models import Post
from users.models import Profile, Follow


# Create your views here.

class UserDetailView(LoginRequiredMixin, DetailView):
    """User detail view. Independientemente si es propio o de otro usuario
    se crea una clase ya que la logica que se va a utilizar es un poco mas robusta."""
    login_url = 'users:login'  # En dado caso de que ingresemos sin usuario nos redireccionará.
    template_name = 'users/detail.html'
    # Actua como una PK ya que no hay usuarios repetidos.
    slug_field = 'username'
    # Es el valor que se le agergará en cada campo al buscar un perfil.
    slug_url_kwarg = 'username'
    # Aqui importamos todos los datos de usuairos y procesarlos segun la accion.
    queryset = User.objects.all()
    # Este será el nombre del objeto que manejaremos en las templates.
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        follower = self.request.user  # Corresponde al following_update
        
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        context['posts_count'] = Post.objects.filter(user=user).count()
        context['following_count'] = Follow.objects.filter(
            follower=user).count()
        context['followers_count'] = Follow.objects.filter(
            following=user).count()
        context['following_update'] = Follow.objects.filter(
            follower=follower, following=user).count()
        context['unread_notifi'] = self.request.unread_notifi
        
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
        """Creamos la "URL" con el nombre de usuario obtenido mediante self."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username': username})

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        context['unread_notifi'] = self.request.unread_notifi
        return context


@login_required
def delete_user(request):
    user = request.user

    if request.method == 'POST':
        # Eliminar el usuario
        user.delete()
        logout(request)
        return redirect('users:login') 
    
    context = {'unread_notifi': request.unread_notifi}
    
    return render(request, 'users/delete_user.html', context)


@login_required
def delete_picture(request):
    user = request.user
    
    if request.method == "POST":
        if user.profile.picture:
            user.profile.picture.delete()
            
        return redirect("users:update")
 
    context = {'unread_notifi': request.unread_notifi}

    return render(request, 'users/delete_picture.html', context)


class SignUpView(FormView):
    """Users sign up. Utilizando "FromView" """
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
    template_name = 'users/logged_out.html'  # Esta direccion no será requerida para el proceso pero si para declarar la funcion.


@login_required
def FollowView(request, username):
    user = request.user  # Usuario logeado
    # Traemos al modelo user del usuario visitado
    following = get_object_or_404(User, username=username)
    follow = Follow.objects.filter(follower=user, following=following).count()
    if not follow:
        follow = Follow.objects.create(follower=user, following=following)
        # follow.save() #no se guarda porque crea dos parametros
    else:
        follow = Follow.objects.filter(
            follower=user, following=following).delete()

    return HttpResponseRedirect(reverse('users:detail', args=[username]))


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
    login_url = 'users:login'  # En dado caso de que ingresemos sin usuario nos redireccionará.
    template_name = 'users/followers.html'
    # Actua como una PK ya que no hay usuarios repetidos.
    slug_field = 'username'
    # Es el valor que se le agergará en cada campo al buscar un perfil.
    slug_url_kwarg = 'username'
    # Aqui importamos todos los datos de usuairos y procesarlos segun la accion.
    queryset = User.objects.all()
    # Este será el nombre del objeto que manejaremos en las templates.
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        # Filtramos para buscar quienes siguen a nuestro usuario actual
        followers_filter_names = Follow.objects.filter(following=user)
        followers_names = [
            names.follower.username for names in followers_filter_names]
        followers_names = sorted(followers_names)

        # Obtenemos los modelos con la lista obtenida anteriormente.
        users_filter = User.objects.filter(username__in=followers_names)
        # print(users_filter)
        context['users_filter'] = users_filter

        return context


class FollowingView(LoginRequiredMixin, DetailView):  # Clase de la view Following
    login_url = 'users:login'
    template_name = 'users/following.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        # Filtramos para buscar quienes siguen a nuestro usuario actual
        following_filter_names = Follow.objects.filter(follower=user)
        # Obtenemos una lista de nombres
        following_names = [
            names.following.username for names in following_filter_names]
        following_names = sorted(following_names)  # Ordenamos los datos
        # Obtenemos los modelos con la lista obtenida anteriormente.
        users_filter = User.objects.filter(username__in=following_names)

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

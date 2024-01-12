"""Posts views."""

# Django 
from django.contrib.auth.decorators import login_required # Decorador para mostrar contenido si estamos logeados.
from django.shortcuts import render, redirect #Ahora si utilizaremos render
from django.contrib.auth.mixins import LoginRequiredMixin # Modulo para asefurar las classes de vistas.
from django.views.generic import CreateView, DetailView, ListView # Se utiliza para crear vistas que rendericen una lista de objetos desde una base de datos, como por ejemplo, mostrar una lista de usuarios, publicaciones de un blog
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Forms
from posts.forms import PostForm
from comment.forms import CommentForm

# Model
from posts.models import Post, Like
from comment.models import Comment
from users.models import Profile
from django.contrib.auth.models import User

# Create your views here.

class PostsFeedView(LoginRequiredMixin, ListView):  # Clase para la paginacion.
    """Return all published posts."""
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 20
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener datos de otro modelo (en este caso, Like)
        likes = Like.objects.filter(user=self.request.user)  
        
        
        # Filtrar likes del usuario actual
        liked_posts = [like.post.id for like in likes] #Aqui ingresamos a la "id" del modelo "Post" mediante la fk.
        #liked_posts = [like.post_id for like in likes] #Ambos funcionan "aqui ingresamos directamente al valor post_id del modelo likes"
        # Agregar los datos de Like al contexto
        
        # Obtener comentarios para cada post en la lista
        comment_counts = {}
        for post in context['post']:
            comments = Comment.objects.filter(post=post)
            comment_counts[post.user.username] = comments.count()
        
        print(comment_counts)
        context['comment_counts'] = comment_counts
        context['liked_posts'] = liked_posts #Esto es para saber si el usuario actual ya dio like
        

        return context



class PostDetailView(LoginRequiredMixin, DetailView):
    """Return detail posts."""
    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener datos de otro modelo (en este caso, Like)
        likes = Like.objects.filter(user=self.request.user)  
        liked_posts = [like.post.id for like in likes] # Filtrar likes del usuario actual

        # Obtenemos los comentarios de cada post
        post = self.get_object() #Cachamos al objecto actual llamado post
        comment = Comment.objects.filter(post=post).order_by("-date")
        users_names = [names.user.username for names in comment]
        
        users_filter = User.objects.filter(username__in=users_names)
        #profiles = Profile.objects.filter(user__in=users_filter)
        
        #print(profiles)
        #print(type(profiles))
        # Agregar los datos de Like al contexto
        context['liked_posts'] = liked_posts
        context['comment']= comment
        context['comment_form'] = CommentForm(initial={'user': self.request.user})
        context['comment'] = comment
        context['comment_count'] = comment.count()
        context['users_filter'] = users_filter

        return context

    def post(self, request, *args, **kwargs):
        #post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post = self.get_object()
        #print("bandera 1")
        comment_form = CommentForm(request.POST)
        #print("bandera 2")
        if comment_form.is_valid():
            #print("bandera 3")
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('posts:detailPost', args=[str(post.id)]))
        #print("bandera 4")
        
        context = self.get_context_data(**kwargs)
        context['comment_form'] = comment_form
        
        return render(request, 'post/detail.html', context )
    
    
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

@login_required
def LikesView(request, post_id):
    user = request.user #Identificamos al usuario actual.
    post = Post.objects.get(id=post_id) #Obtenemos el post actual.
    current_likes = post.likes #Verificamos cuantos likes tiene el post.
    liked = Like.objects.filter(user=user, post=post).count()
    if not liked:
        liked = Like.objects.create(user=user, post=post)
       
        liked.save()
        
        current_likes = current_likes + 1
    else:
        liked = Like.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
        
    
    post.likes = current_likes
    post.save()
    
    return  HttpResponseRedirect(reverse('posts:feed'))
    # return  HttpResponseRedirect(reverse('posts:detailPost', args=[post_id]))
        

     
    
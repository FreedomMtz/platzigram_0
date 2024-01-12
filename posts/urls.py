"""Posts URLs."""

#Django
from django.urls import path

#Views
from posts import views # Aqui se habia definido como as post_views. Pero ya no es necesario.

urlpatterns = [
    
    #Managment
    path(
        route='', 
        view=views.PostsFeedView.as_view(), 
        name='feed'
    ), # Agregaremos una vista de la app "posts"
    
    path(
        route='posts/new', 
        view=views.CreatePostView.as_view(), 
        name="create"
    ), # Agregamos la vista para crear un nuevo post.
    
    ###Solucion del reto por parte del profe
    
    path(
        route='posts/<int:pk>/', #post.id
        view=views.PostDetailView.as_view(),
        name='detailPost'
    ),
    
    path(
        route='posts/<int:post_id>/like',
        view=views.LikesView,
        name="postLike"
    )

]

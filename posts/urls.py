"""Posts URLs."""

# Django
from django.urls import path

# Views
# Aqui se habia definido como as post_views. Pero ya no es necesario.
from posts import views

urlpatterns = [

    # Managment
    path(
        route='',
        view=views.PostsFeedView.as_view(),
        name='feed'
    ),  # Agregaremos una vista de la app "posts"

    path(
        route='posts/new',
        view=views.CreatePostView.as_view(),
        name="create"
    ),  # Agregamos la vista para crear un nuevo post.

    # Solucion del reto por parte del profe

    path(
        route='posts/<int:pk>/',  # post.id, pk
        view=views.PostDetailView.as_view(),
        name='detailPost'
    ),

    path(
        route='posts/<int:post_id>/like',
        view=views.LikesView,
        name="postLike"
    ),

    path(
        route='posts/<int:post_id>/update',
        view=views.UpdatePostView.as_view(),
        name="postUpdate"
    ),

    path(
        route='posts/<int:pk>/delete',
        view=views.PostDeleteView.as_view(),
        name="postDelete"
    ),

    path(
        route='posts/<int:pk>/<int:id>/comment_delete',
        view=views.DeleteCommentView.as_view(),
        name="commentDelete"
    ),

    path(
        route='posts/<int:post_pk>/<int:comments_id>/update_comment',
        view=views.UpdateCommentView.as_view(),
        name="commentUpdate"
    ),

]

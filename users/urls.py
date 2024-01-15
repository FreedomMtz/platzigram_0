"""Users URLs."""

#Django
from django.urls import path



#Views
from users import views # Aqui se habia definido como as user_views. Pero ya no es necesario.

urlpatterns = [
    
   
    #Solucion al reto propio
    #path(
    #    route='profile/<str:username>/<int:id>/', 
    #    view=views.PostDetailView.as_view(), 
    #    name="detailPost"
    #),
    
    #Managment
    path(
        route='login/',
        view=views.LoginView.as_view(), 
        name='login'
    ), # Agregamos la vista para ingresar a la app.
    path(
        route='logout/',
        view=views.LogoutView.as_view(), 
        name='logout'
    ), # Agregamos la vista para salir de la app.
    path(
        route='signup/',
        view=views.SignUpView.as_view(), 
        name="signup"
    ), # Agregamos la vista para registrarse en la app.
    path(
        route='me/profile/',
        view=views.UpdateProfileView.as_view(), 
        name="update"
    ), # Agregamos la vista para modificar nuestro perfil.
    
    path(
        route='me/profile/delete_photo',
        view=views.delete_picture, 
        name="deletePicture"
    ), # Agregamos la vista para eliminar nuestra foto de perfil.
    
    
     #Posts
    path(
        route='profile/<str:username>/',
        view=views.UserDetailView.as_view(),
        name='detail'     
    ),
    
    path(
        route='profile/<str:username>/follow',
        view=views.FollowView,
        name="follow"
    ),
    
    path(
        route='profile/<str:username>/followers',
        view=views.FollowerView.as_view(),
        name="followers"
    ),
    
    path(
        route='profile/<str:username>/following',
        view=views.FollowingView.as_view(),
        name="following"
    ),
    
    path(
        route='me/profile/delete_profile',
        view=views.delete_user, 
        name="deleteUser"
    ) # Agregamos la vista para eliminar nuestro perfil y usuario.
    
    
    
]





"""Directs URLs."""

#Django
from django.urls import path

#Views
from directs import views # Aqui se habia definido como as post_views. Pero ya no es necesario.

urlpatterns = [
    
    #Managment
    path(
        route='inbox/', 
        view=views.inbox, 
        name='message'
    ), # Agregaremos una vista de la app "directs" para el inbox
    
    path(
        route='directs/<str:username>/', 
        view=views.directs, 
        name='direct'
    ), # Agregaremos una vista de la app "directs" para chat personal
    
    path(
        route='send/', 
        view=views.SendMessage, 
        name='sendMessage'
    ), # Agregaremos una vista de la app "directs" para enviar mensajes
    
    path(
        route='search/', 
        view=views.UserSearch, 
        name='userSearch'
    ), # Agregaremos una vista de la app "directs" para buscar un usuario
    
    path(
        route='new/<str:username>', 
        view=views.NewMessage, 
        name='newMessage'
    ), # Agregaremos una vista de la app "directs" para crear un nuevo mensajes
    
    path(
        route='delete/<str:username>', 
        view=views.DeleteMessage, 
        name='deleteMessage'
    ), # Agregaremos una vista de la app "directs" para eliminar conversacion actual.
    
]
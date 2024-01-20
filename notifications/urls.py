"""Notifications URLs."""

# Django
from django.urls import path

# Views
from notifications import views

urlpatterns = [

    # Managment
    path(
        route='',
        view=views.ShowNotifications,
        name='showNotifi'
    ),  # Agregamos la vista para ver las notificaciones de la app "Notifications"

    path(
        route='delete/<int:noti_id>',
        view=views.DeleteNotifications,
        name='deleteNotifi'
    ),
]

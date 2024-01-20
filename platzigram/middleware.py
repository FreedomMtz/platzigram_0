"""Platzigram middleware catalog."""

# Django
# Ajusta el import según la ubicación real de tu modelo Message
from directs.models import Message
from typing import Any
from django.shortcuts import redirect
from django.urls import reverse

# middleware.py


class ProfileCompletionMiddlewere:
    """Profile completion middlewere.
    Ensure every user that is interacting with the plataform
    have their profile picture and biography.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Code to be executed for each request before the view is called"""
        if not request.user.is_anonymous:
            if not request.user.is_staff:
                profile = request.user.profile
                if not profile.user.profile:
                    if request.path not in [reverse('users:update'), reverse('users:logout')]:
                        return redirect('users:update')
               
        response = self.get_response(request)
        return response


class NotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lógica para obtener el valor de unread_notifi
        if not request.user.is_anonymous:
            messages = Message.get_message(user=request.user)
            unread_notifi = sum(
                message['unread'] for message in messages if message['unread'] != request.user)

            # Adjunta el valor al objeto de solicitud para que esté disponible en las vistas
            request.unread_notifi = unread_notifi

        # Continúa con la cadena de middleware y las vistas
        response = self.get_response(request)

        return response

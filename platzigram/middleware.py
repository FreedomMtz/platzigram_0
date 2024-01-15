"""Platzigram middleware catalog."""

# Django
from typing import Any
from django.shortcuts import redirect
from django.urls import reverse


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
                print("bandera1")
                profile = request.user.profile
                if not profile.user.profile:
                    if request.path not in [reverse('users:update'), reverse('users:logout')]:
                        print("bandera2")
                        return redirect('users:update')
                print("bandera3")
        response = self.get_response(request)
        return response
    
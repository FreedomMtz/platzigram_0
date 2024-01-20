"""Users forms."""

# Django
from django import forms

# Models
from django.contrib.auth.models import User
from users.models import Profile


class SignupForm(forms.Form):
    """Sign up form."""
    username = forms.CharField(min_length=4, max_length=50)
    password = forms.CharField(max_length=70, widget=forms.PasswordInput())
    password_confirmation = forms.CharField(
        max_length=70, widget=forms.PasswordInput())
    first_name = forms.CharField(min_length=2, max_length=50)
    last_name = forms.CharField(min_length=2, max_length=50)
    email = forms.CharField(min_length=6, max_length=30,
                            widget=forms.EmailInput())
    """Antes de pasar el dato del username, primero lo limpearemos"""

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('Username is already in use.')
        else:
            
            return username

    """Lo mismo aremos para el email."""

    def clean_email(self):
        """Email must be unique."""
        email = self.cleaned_data['email']
        email_taken = User.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('Email is already in use.')
        else:
            
            return email
    """La comparacion de elementos del mismo "form" se hacen en orden y este se ejecuta al final"""

    def clean(self):
        """Verify password confimation match"""
        data = super().clean()
        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Password do not match.')
        else:
            
            return data

    def save(self):
        """Create user and profile."""
        data = self.cleaned_data
        # Excluimos un dato (no esta definido en nuestro modelo).
        data.pop('password_confirmation')
        # Podriamos enviar como (email=data['email'],..) |(**data) envía.todos.los.datos.
        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()

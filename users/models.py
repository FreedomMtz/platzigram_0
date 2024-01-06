"""Users models."""

# Django.
from django.contrib.auth.models import User # Importamos un modelo llamado "User" para customizarlo.
from django.db import models

# Create your models here.
class Profile(models.Model):
    """Profile model."""
    """Proxy model/modelo intermediario que utilizaremos para customizar nuestro registro
    de usuarios para nuestra aplicacion"""
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Nos aseguramos que exista un solo usuario. Y si se elimina la secuencia sera en CASCADA (se elimina contenido que este referenciado al usuario).
    
    website = models.URLField(max_length=200, blank=True) # Creamos un campo para una URL y puede estar en blanco.
    biography = models.TextField(max_length=500, blank=True) # Campo para la biografia.
    phone_number = models.CharField(max_length=20, blank=True) # Campo para el numero telefónico.
    
    picture = models.ImageField(upload_to='users/pictures', 
                                blank=True, 
                                null=True
                                ) # Campo para la foto.
    
    created = models.DateTimeField(auto_now_add=True) # Campo para registro de creación.
    modified = models.DateTimeField(auto_now=True) # Campo para registro de modificación.
    
    def __str__(self):
        """Return username."""
        return self.user.username
    
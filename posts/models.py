"""Posts models."""
# Django
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Models es un módulo en Django que proporciona herramientas y clases para definir la estructura de 
# la base de datos mediante modelos

# Model es una clase base proporcionada por Django que se utiliza para definir modelos de datos (tablas). 
# EmailField, CharField...son los tipos de datos que tendran cada columna.

# Reestructuraremos al modelo POST
class Post(models.Model):
    """Post model."""
    user = models.ForeignKey(User,on_delete=models.CASCADE) # Relacionamos mediante la "foreignkey" al modelo User "ADMIN".
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE) # Relacionamos mediante la "foreignkey" al modelo Profile.
    
    title = models.CharField(max_length=255) # Creamos al campo del titulo.
    photo = models.ImageField(upload_to='post/photos') # Creamos el campo y ruta de almacenamiento de las fotos.
    
    created = models.DateTimeField(auto_now_add=True) # Creamos los campos para la fecha de creación. 
    modified = models.DateTimeField(auto_now=True) # Creamos los campos para la fecha de modificación 
    
    def __str__(self):  # Definimo que mostrar al ejecutar un QUERRY
        """Return title and username."""
        return '{} by @{}'.format(self.title, self.user.username)
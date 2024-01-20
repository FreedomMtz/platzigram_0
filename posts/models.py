"""Posts models."""
# Django
from django.db import models
from django.db.models.signals import post_save, post_delete

# Models
from django.contrib.auth.models import User
from notifications.models import Notification


class Post(models.Model):
    """Post model."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)  # Relacionamos mediante la "foreignkey" al modelo User "ADMIN".
    # Relacionamos mediante la "foreignkey" al modelo Profile.
    profile = models.ForeignKey('users.Profile', on_delete=models.CASCADE)

    title = models.CharField(max_length=255)  # Creamos al campo del titulo.
    # Creamos el campo y ruta de almacenamiento de las fotos.
    photo = models.ImageField(upload_to='post/photos')

    # Creamos los campos para la fecha de creación.
    created = models.DateTimeField(auto_now_add=True)
    # Creamos los campos para la fecha de modificación
    modified = models.DateTimeField(auto_now=True)
    # Agregamos una variable que serivrá como contador de likes.
    likes = models.IntegerField(default=0)

    def __str__(self):  # Definimos que mostrar al ejecutar un QUERRY
        """Return title and username."""
        return '{} by @{} likes:{}'.format(self.title, self.user.username, self.likes)


class Like(models.Model):
    # Fk para el modelo User.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_likes")
    # Fk para el modelos Posts.
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_likes")

    def user_liked_post(sender, instance, *args, **kwargs):
        like = instance
        sender = like.user
        post = like.post

        notify = Notification(post=post, sender=sender,
                              user=post.user, notification_type=1)
        notify.save()

    def user_unlike_post(sender, instance, *args, **kwargs):
        like = instance
        sender = like.user
        post = like.post

        notify = Notification.objects.filter(
            post=post, sender=sender, notification_type=1)
        notify.delete()


# Like model
post_save.connect(Like.user_liked_post, sender=Like)
post_delete.connect(Like.user_unlike_post, sender=Like)


# NOTAS:
# Models es un módulo en Django que proporciona herramientas y clases para definir la estructura de
# la base de datos mediante modelos
# Model es una clase base proporcionada por Django que se utiliza para definir modelos de datos (tablas).
# EmailField, CharField...son los tipos de datos que tendran cada columna.
# Reestructuraremos al modelo POST

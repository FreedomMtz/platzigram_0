"""Users models."""
# Django.
# Importamos un modelo llamado "User" para customizarlo.
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

# Models.
from django.db import models
from notifications.models import Notification
# Create your models here.


class Profile(models.Model):
    """Profile model."""
    """Proxy model/modelo intermediario que utilizaremos para customizar nuestro registro
    de usuarios para nuestra aplicacion"""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE)  # Nos aseguramos que exista un solo usuario. Y si se elimina la secuencia sera en CASCADA (se elimina contenido que este referenciado al usuario).
    # Creamos un campo para una URL y puede estar en blanco.
    website = models.URLField(max_length=200, blank=True)
    # Campo para la biografia.
    biography = models.TextField(max_length=500, blank=True)
    # Campo para el numero telefónico.
    phone_number = models.CharField(max_length=20, blank=True)
    picture = models.ImageField(upload_to='users/pictures',
                                blank=True,
                                null=True
                                )  # Campo para la foto.

    # Campo para registro de creación.
    created = models.DateTimeField(auto_now_add=True)
    # Campo para registro de modificación.
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return username."""
        return self.user.username

# Modelo para relacionar los Followers


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")

    def user_follow(sender, instance, *args, **kargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notification(
            sender=sender, user=following, notification_type=3)
        notify.save()

    def user_unfollow(sender, instance, *args, **kargs):
        follow = instance
        sender = follow.follower
        following = follow.following

        notify = Notification.objects.filter(
            sender=sender, user=following, notification_type=3)
        notify.delete()


# Follow signals
post_save.connect(Follow.user_follow, sender=Follow)
post_delete.connect(Follow.user_unfollow, sender=Follow)

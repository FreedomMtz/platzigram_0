# Django
from django.db import models

# Models
from django.contrib.auth.models import User


# Create your models here.

class Notification(models.Model):

    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Comment'), (3, 'Follow'))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="noti_to_user")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="noti_from_user")
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE,
                             related_name="noti_post", blank=True, null=True)
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):  # Definimo que mostrar al ejecutar un QUERRY
        return '{} by @ {} post:{} read:{}'.format(self.notification_type, self.sender.username, self.post, self.is_seen)

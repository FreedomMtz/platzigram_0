# Django
from django.db import models
from django.contrib.auth.models import User

# Models
from posts.models import Post

# Create your models here.
class Comment(models.Model):
    """ Comments model. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{} by @{}'.format(self.body, self.user.username)
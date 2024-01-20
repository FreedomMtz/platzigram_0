# Django
from django.db import models
from django.db.models.signals import post_save, post_delete

# Models
from django.contrib.auth.models import User
from posts.models import Post
from notifications.models import Notification

class Comment(models.Model):
    """ Comments model. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField(max_length=500, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} by @{}'.format(self.body, self.user.username)

    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user

        notify = Notification(post=post, sender=sender, user=post.user,
                              text_preview=text_preview, notification_type=2)
        notify.save()

    def user_delete_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        sender = comment.user

        notify = Notification.objects.filter(
            post=post, sender=sender, user=post.user, notification_type=2)
        notify.delete()


# Follow
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_delete_comment_post, sender=Comment)

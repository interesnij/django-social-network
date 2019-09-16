from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from notifications.models.notification import Notification


class PostCommentNotification(models.Model):
    notification = GenericRelation(Notification, related_name='post_comment_notifications')
    post_comment = models.ForeignKey('posts.PostComment', on_delete=models.CASCADE,verbose_name="О комментарии к посту")

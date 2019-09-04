from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from notifications.models.notification import Notification
from posts.models import PostUserMention


class PostUserMentionNotification(models.Model):
    notification = GenericRelation(Notification, related_name='post_user_mention_notifications')
    post_user_mention = models.ForeignKey(PostUserMention, on_delete=models.CASCADE,verbose_name="На упоминание в посте")

    

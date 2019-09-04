from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from notifications.models.notification import Notification
from posts.models import PostReaction


class PostReactionNotification(models.Model):
    notification = GenericRelation(Notification, related_name='post_reaction_notifications')
    post_reaction = models.ForeignKey(PostReaction, on_delete=models.CASCADE,verbose_name="Реакция на пост")

    

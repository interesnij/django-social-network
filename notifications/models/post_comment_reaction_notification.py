from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from notifications.models.notification import Notification
from posts.models import PostCommentReaction



class PostCommentReactionNotification(models.Model):
    notification = GenericRelation(Notification, related_name='post_comment_reaction_notifications')
    post_comment_reaction = models.ForeignKey(PostCommentReaction, on_delete=models.CASCADE,verbose_name="Рекция на комментарий к посту")

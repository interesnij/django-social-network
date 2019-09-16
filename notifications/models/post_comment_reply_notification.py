from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from notifications.models.notification import Notification



class PostCommentReplyNotification(models.Model):
    notification = GenericRelation(Notification, related_name='post_comment_reply_notifications')
    #post_comment = models.ForeignKey('posts.PostComment', on_delete=models.CASCADE,verbose_name="На ответ к комментарию к посту")

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from notifications.models.notification import Notification
from posts.models import PostCommentUserMention


class PostCommentUserMentionNotification(models.Model):
    notification = GenericRelation(Notification, related_name='post_comment_user_mention_notifications')
    #post_comment_user_mention = models.ForeignKey(PostCommentUserMention, on_delete=models.CASCADE,verbose_name="На упоминание в комментарии к посту")

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from notifications.models.notification import Notification


class PostCommentUserMentionNotification(models.Model):
    notification = GenericRelation(Notification, related_name='post_comment_user_mention_notifications')
    #post_comment_user_mention = models.ForeignKey('posts.PostCommentUserMention', on_delete=models.CASCADE,verbose_name="На упоминание в комментарии к посту")

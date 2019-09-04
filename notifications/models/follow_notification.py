from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from notifications.models.notification import Notification
from users.models import User


class FollowNotification(models.Model):
    notification = GenericRelation(Notification)
    follower = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Подписка")

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Q
from notifications.models.notification import Notification
from users.models import User


class ConnectionRequestNotification(models.Model):
    notification = GenericRelation(Notification)
    connection_requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+',verbose_name="Запрос в друзья")

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from users.models import User
from notifications.models.notification import Notification


class ConnectionConfirmedNotification(models.Model):
    notification = GenericRelation(Notification)
    connection_confirmator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+',verbose_name="Подтверждение заявки в друзья")

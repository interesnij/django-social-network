from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from notifications.models.notification import Notification


class CommunityInviteNotification(models.Model):
    notification = GenericRelation(Notification)
    #community_invite = models.ForeignKey('communities.CommunityInvite', on_delete=models.CASCADE,verbose_name="Приглашение в сообщество")

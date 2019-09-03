from django.conf import settings
from django.db import models
from django.utils import timezone
from common.models import Emoji
#from follows.models import Follow
from users.models import User



class List(models.Model):
    #creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists',verbose_name="Создатель")
    emoji = models.ForeignKey(Emoji, on_delete=models.SET_NULL, related_name='lists', null=True,verbose_name="Смайл")
    name = models.CharField(max_length=settings.100, blank=False, null=False,verbose_name="Название")
    #follows = models.ManyToManyField(Follow, related_name='lists', db_index=True,verbose_name="Подписчики")
    created = models.DateTimeField(editable=False,verbose_name="Создан")

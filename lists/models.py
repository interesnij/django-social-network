from django.db import models
from django.utils import timezone
from follows.models import Follow
from users.models import User



class List(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lists',verbose_name="Создатель")
    name = models.CharField(max_length=100, blank=False, null=False,verbose_name="Название")
    follows = models.ManyToManyField(Follow, related_name='lists', db_index=True,verbose_name="Подписчики")
    created = models.DateTimeField(default=timezone.now, editable=False,verbose_name="Создан")

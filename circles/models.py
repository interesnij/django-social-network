from django.conf import settings
from django.db import models
from django.utils import timezone
#from connections.models import Connection
#from posts.models import Post
from django.utils import timezone


class ConnectionCircle(models.Model):
    #connection = models.ForeignKey(Connection, on_delete=models.CASCADE,verbose_name="Соединение")
    circle = models.ForeignKey('circles.Circle', on_delete=models.CASCADE,verbose_name="Круг")



class Circle(models.Model):
    #creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='circles', null=True, verbose_name="Создатель")
    name = models.CharField(max_length=100, blank=False, null=False,verbose_name="Название")
    #posts = models.ManyToManyField(Post, related_name='circles', db_index=True, verbose_name="Посты")
    #connections = models.ManyToManyField(Connection, related_name='circles', db_index=True, verbose_name="Соединение")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создан")

    def __str__(self):
        return self.name

from django.conf import settings
from django.db import models
from django.utils import timezone
from communities.models import Community
#from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False,
                            unique=True,verbose_name="Название")
    description = models.CharField(max_length=300, blank=False,
                                   null=True,verbose_name="Описание" )
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Когда создана")
    avatar = models.ImageField(blank=False, null=True,verbose_name="Аватар")

    order = models.IntegerField(unique=False, default=0,verbose_name="Порядковый номер")
    #creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_categories', null=True, verbose_name="Создатель")
    communities = models.ManyToManyField(Community, related_name='categories', blank=True,verbose_name="Сообщество")

    def __str__(self):
        return 'Категория: ' + self.name

from django.db import models
from django.utils import timezone


class EmojiGroup(models.Model):
    keyword = models.CharField(max_length=32, blank=False, null=False, verbose_name="Слово")
    order = models.IntegerField(unique=False, default=100,verbose_name="Порядковый номер")
    created = models.DateTimeField(editable=False,verbose_name="Создана")
    is_reaction_group = models.BooleanField(default=False,verbose_name="Это реакция группы")



class Emoji(models.Model):
    group = models.ForeignKey(EmojiGroup, on_delete=models.CASCADE, related_name='emojis', null=True,verbose_name="Группа")
    keyword = models.CharField(max_length=16, blank=False, null=False,verbose_name="Слово")
    image = models.ImageField(blank=False, null=False,verbose_name="Изображение")
    created = models.DateTimeField(editable=False,verbose_name="Создан")
    order = models.IntegerField(unique=False, default=100,verbose_name="Порядковый номер")

    def __str__(self):
        return 'Смайлы: ' + self.keyword



class Badge(models.Model):
    keyword = models.CharField(max_length=16, blank=False, null=False, unique=True,verbose_name="Слово")
    keyword_description = models.CharField(max_length=64, blank=True, null=True, unique=True,verbose_name="Описание")
    created = models.DateTimeField(editable=False,verbose_name="Создан")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Badge, self).save(*args, **kwargs)

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone



class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        return self.get_queryset().filter(vote__lt=0)

    def posts(self):
        return self.get_queryset().filter(content_type__model='posts').order_by('-posts__created')
    def comments(self):
        return self.get_queryset().filter(content_type__model='comment').order_by('-comments__created')

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Не нравится'),
        (LIKE, 'Нравится')
    )

    vote = models.SmallIntegerField(verbose_name="Голос", choices=VOTES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    objects = LikeDislikeManager()


class Badge(models.Model):
    keyword = models.CharField(max_length=16, blank=False, null=False, unique=True, verbose_name="Слово")
    keyword_description = models.CharField(max_length=64, blank=True, null=True, unique=True, verbose_name="Описание")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создан")

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(Badge, self).save(*args, **kwargs)


class Item(models.Model):
    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_creator', verbose_name="Создатель")
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_closed = models.BooleanField(default=False, verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    views=models.IntegerField(default=0, verbose_name="Просмотры")

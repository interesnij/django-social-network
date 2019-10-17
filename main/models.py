import uuid
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Sum
from django.conf import settings
from django.utils import timezone
from django.contrib.postgres.indexes import BrinIndex
from django.db import transaction


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


class Item(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True,verbose_name="uuid")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, related_name='communa', null=True, blank=True, verbose_name="Сообщество")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='creator', verbose_name="Создатель")
    is_edited = models.BooleanField(default=False, verbose_name="Изменено")
    is_closed = models.BooleanField(default=False, verbose_name="Закрыто")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалено")
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    views=models.IntegerField(default=0, verbose_name="Просмотры")
    votes = GenericRelation(LikeDislike, related_query_name='article')
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='item')


    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )
        index_together = [('creator', 'community'),]

    def save(self, *args, **kwargs):
        if not self.is_fixed:
            return super(Item, self).save(*args, **kwargs)
        with transaction.atomic():
            Item.objects.filter(
                is_fixed=True).update(is_fixed=False)
            return super(Item, self).save(*args, **kwargs)

    def fixed(self):
        item = Item.objects.get(id=self.id)
        item.is_fixed=True
        return item

    def unfixed(self):
        item = Item.objects.get(id=self.id)
        item.is_fixed=False
        return item


class Comment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='article_replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_comments',verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаено")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, related_name='article_comments')

    class Meta:
        indexes = (
            BrinIndex(fields=['created']),
        )

    def count_replies(self):
        return self.replies.count()

    def get_replies(self):
        get_comments = Comment.objects.filter(parent_comment=self).all()
        return get_comments

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

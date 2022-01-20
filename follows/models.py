from django.db import models
from django.conf import settings


class Follow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='follows', verbose_name="Подписчик")
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='followers', null=False, verbose_name="На кого подписывается")
    view = models.BooleanField(default=False, verbose_name="Просмотрено")
    visited = models.PositiveIntegerField(default=0, verbose_name="Количество визитов")

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


    @classmethod
    def create_follow(cls, user_id, followed_user_id):
        return cls.objects.create(user_id=user_id, followed_user_id=followed_user_id,)


class CommunityFollow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='community_follows', verbose_name="Подписчик")
    community = models.ForeignKey('communities.Community', db_index=False, on_delete=models.CASCADE, related_name='community', null=False, verbose_name="На какое сообщество подписывается")
    view = models.BooleanField(default=False, verbose_name="Просмотрено")
    visited = models.PositiveIntegerField(default=0, verbose_name="Количество визитов")

    class Meta:
        unique_together = ('user', 'community')
        verbose_name = 'Подписчик группы'
        verbose_name_plural = 'Подписчики группы'


    @classmethod
    def create_follow(cls, user_id, community_pk):
        return cls.objects.create(user_id=user_id, community_pk=community_pk)

    @classmethod
    def get_community_with(cls, community_pk):
        return cls.objects.filter(community__pk=community_pk, view=False)

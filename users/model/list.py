from django.conf import settings
from django.db import models
from django.db.models import Q


class UserBlock(models.Model):
    blocked_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='blocked_by_users', verbose_name="Кого блокирует")
    blocker = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='user_blocks', verbose_name="Кто блокирует")

    @classmethod
    def create_user_block(cls, blocker_id, blocked_user_id):
        return cls.objects.create(blocker_id=blocker_id, blocked_user_id=blocked_user_id)

    @classmethod
    def users_are_blocked(cls, user_a_id, user_b_id):
        return cls.objects.filter(Q(blocked_user_id=user_a_id, blocker_id=user_b_id)).exists()

    class Meta:
        unique_together = ('blocked_user', 'blocker',)
        indexes = [models.Index(fields=['blocked_user', 'blocker']),]

class ListUC(models.Model):
    NO, MAIN, LIST = 0, 1, 2
    TYPE = (
        (MAIN, 'Основной список'),(LIST, 'Пользовательский'),(NO, 'Нет значения'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE, default=NO, verbose_name="Тип списка")
    name = models.CharField(max_length=100)
    owner = models.PositiveIntegerField(default=0, verbose_name="Владелец")


class FeaturedUC(models.Model):
    list = models.ForeignKey(ListUC, db_index=False, on_delete=models.CASCADE, related_name='+', verbose_name="Список")
    owner = models.PositiveIntegerField(default=0, verbose_name="Кто получает")
    user = models.PositiveIntegerField(default=0, verbose_name="Рекомендуемый друг")
    community = models.PositiveIntegerField(default=0, verbose_name="Рекомендуемое сообщество")
    mute = models.BooleanField(default=False, verbose_name="Источник скрыт")
    sleep = models.DateTimeField(blank=True, null=True, verbose_name='Не показывать до...')

    class Meta:
        verbose_name = 'Источник рекомендаций'
        verbose_name_plural = 'Источники рекомендаций'
        constraints = [
            models.UniqueConstraint(fields=['owner', 'user', 'community'], name='feature_uc')
        ]

    def __str__(self):
        if self.user:
            return "Кому рекомендуют: " + str(self.owner) + ", возможный друг: " + str(self.user)
        elif self.community:
            return "Кому рекомендуют: " + str(self.owner) + ", возможная группа: " + str(self.community)


    def is_open(self):
        if self.mute:
            return False
        elif not sleep:
            return True
        else:
            from datetime import datetime
            return self.sleep < datetime.now()

class NewsUC(models.Model):
    list = models.ForeignKey(ListUC, db_index=False, on_delete=models.CASCADE, related_name='+', verbose_name="Список")
    owner = models.PositiveIntegerField(default=0, verbose_name="Кто получает")
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    community = models.PositiveIntegerField(default=0, verbose_name="Сообщество")
    mute = models.BooleanField(default=False, verbose_name="Источник скрыт")
    sleep = models.DateTimeField(blank=True, null=True, verbose_name='Не показывать до...')

    class Meta:
        verbose_name = 'Источник новостей'
        verbose_name_plural = 'Источники новостей'
        constraints = [
            models.UniqueConstraint(fields=['owner', 'user', 'community'], name='news_uc')
        ]

    def __str__(self):
        if self.user:
            return "Кто получает новости: " + str(self.owner) + ", от пользователя: " + str(self.user)
        elif self.community:
            return "Кто получает новости: " + str(self.owner) + ", от группы: " + str(self.community)

    def is_open(self):
        if self.mute:
            return False
        elif not sleep:
            return True
        else:
            from datetime import datetime
            return self.sleep < datetime.now()

class NotifyUC(models.Model):
    list = models.ForeignKey(ListUC, db_index=False, on_delete=models.CASCADE, related_name='+', verbose_name="Список")
    owner = models.PositiveIntegerField(default=0, verbose_name="Кто получает")
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    community = models.PositiveIntegerField(default=0, verbose_name="Сообщество")
    mute = models.BooleanField(default=False, verbose_name="Источник скрыт")
    sleep = models.DateTimeField(blank=True, null=True, verbose_name='Не показывать до...')

    class Meta:
        verbose_name = 'Источник уведомлений'
        verbose_name_plural = 'Источники уведомлений'
        constraints = [
            models.UniqueConstraint(fields=['owner', 'user', 'community'], name='notify_uc')
        ]

    def __str__(self):
        if self.user:
            return "Кто получает уведы: " + str(self.owner) + ", от пользователя: " + str(self.user)
        elif self.community:
            return "Кто получает уведы: " + str(self.owner) + ", от группы: " + str(self.community)

    def is_open(self):
        if self.mute:
            return False
        elif not sleep:
            return True
        else:
            from datetime import datetime
            return self.sleep < datetime.now()


class UserPhotoListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения фотоальбома'
        verbose_name_plural = 'Порядки отображения фотоальбомов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class UserPostsListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка записей'
        verbose_name_plural = 'Порядки отображения списков записей'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class UserPlayListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения плейлиста'
        verbose_name_plural = 'Порядки отображения плейлистов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class UserGoodListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка товаров'
        verbose_name_plural = 'Порядки отображения списков товаров'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class UserVideoListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения видеольбома'
        verbose_name_plural = 'Порядки отображения видеоальбомов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class UserSurveyListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка опросов'
        verbose_name_plural = 'Порядки отображения списков опросов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class UserDocsListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка документов'
        verbose_name_plural = 'Порядки отображения списков документов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

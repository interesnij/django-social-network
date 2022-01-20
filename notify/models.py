from django.db import models
from django.conf import settings
from django.core import serializers
from django.contrib.postgres.indexes import BrinIndex
from notify.helpers import VERB, STATUS, TYPE

"""
итак, ниже у нас уведомления, рассылаемые скопом каждому подписичку на уведомления и управленцу сообществ -
по отношению к другим, и все уведомления, которые применимы к самому пользователю
человек их получает пока подписан на уведомления (состоит в таблице CommunityProfileNotifyб UserProfileNotify).
Он их может их скрывать для себя и отписываться от таблиц выше
"""
class Notify(models.Model):
    recipient = models.ForeignKey('users.User', blank=True, null=True, on_delete=models.CASCADE, related_name='notifications', verbose_name="Получатель")
    creator = models.ForeignKey('users.User', verbose_name="Инициатор", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Класс объекта")
    object_id = models.PositiveIntegerField(default=0, verbose_name="id объекта")
    community = models.ForeignKey('communities.Community', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Сообщество")
    action_community = models.ForeignKey('communities.Community', related_name='+', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def is_have_user_set(self):
        return Notify.objects.filter(user_set_id=self.pk).exists()
    def get_user_set(self):
        return Notify.objects.filter(user_set_id=self.pk) + [self]
    def get_user_set_6(self):
        from django.db.models import Q
        return Notify.objects.filter(Q(id=self) | Q(user_set_id=self.pk))[:6]

    def count_user_set(self):
        count = Notify.objects.filter(user_set_id=self.pk).values("pk").count() + 1
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " запись"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " записи"
        else:
            return str(count) + " записей"
    def get_first_user_set(self):
        return Notify.objects.filter(user_set_id=self.pk).first()

    def is_have_object_set(self):
        return Notify.objects.filter(object_set_id=self.pk).exists()
    def get_object_set(self):
        return Notify.objects.filter(object_set_id=self.pk) + [self]
    def get_object_set_6(self):
        from django.db.models import Q
        from users.models import User
        users = Notify.objects.filter(object_set_id=self.pk).values("creator_id")[:5]
        return User.objects.filter(Q(id=self.creator.pk) | Q(id__in=[i['creator_id'] for i in users]))
    def count_object_set(self):
        count = Notify.objects.filter(object_set_id=self.pk).values("pk").count()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " человек "
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " человека "
        else:
            return str(count) + " людей "
    def get_first_object_set(self):
        return Notify.objects.filter(object_set_id=self.pk).first()

    def show_current_notify(self):
        if self.user_set:
            return self.get_user_set().first()
        elif self.post_set:
            return self.get_post_set().first()
        else:
            return self

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def u_notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, status="U").update(status="R")

    @classmethod
    def c_notify_unread(cls, user_pk, community_id):
        cls.objects.filter(community_id=community_id, status="U").update(status="R")

    def is_unread(self):
        return self.status == "U"

    def get_notify(self, user):
        from common.attach.notify import get_notify
        return get_notify(user, self)


"""
итак, ниже у нас уведомления, создающие ленты новостей. Это получают участники таблиц CommunityNewsNotify, UommunityNewsNotify.
Придется делать еще таблицу игнора кого-то, чтобы не показывать не нужное. Отписался от обновлений человека, создалась запись и
ты свободен от новостей этого пользователя. И тут не нужен получатель(упоминанием человека - он становится creator)
"""
class Wall(models.Model):
    creator = models.ForeignKey('users.User', verbose_name="Инициатор", related_name='creator_wall', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    verb = models.CharField(max_length=5, choices=VERB, verbose_name="Тип уведомления")
    status = models.CharField(max_length=1, choices=STATUS, default="U", verbose_name="Статус")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Класс объекта")
    object_id = models.PositiveIntegerField(default=0, verbose_name="id объекта")
    community = models.ForeignKey('communities.Community', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Сообщество")
    action_community = models.ForeignKey('communities.Community', related_name='+', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Сообщество")

    user_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, человек лайкает несколько постов. Нужно для группировки")
    object_set = models.ForeignKey('self', related_name='+', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Например, несколько человек лайкает пост. Нужно для группировки")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created"]
        indexes = (BrinIndex(fields=['created']),)

    def is_have_user_set(self):
        return Wall.objects.filter(user_set_id=self.pk).exists()
    def get_user_set(self):
        return Wall.objects.filter(user_set_id=self.pk) + [self]
    def get_user_set_6(self):
        from django.db.models import Q
        return Wall.objects.filter(Q(id=self) | Q(user_set_id=self.pk))[:6]

    def count_user_set(self):
        count = Wall.objects.filter(user_set_id=self.pk).values("pk").count() + 1
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " запись"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " записи"
        else:
            return str(count) + " записей"
    def get_first_user_set(self):
        return Wall.objects.filter(user_set_id=self.pk).first()

    def is_have_object_set(self):
        return Wall.objects.filter(object_set_id=self.pk).exists()
    def get_object_set(self):
        return Wall.objects.filter(object_set_id=self.pk) + [self]
    def get_object_set_6(self):
        from django.db.models import Q
        from users.models import User
        users = Wall.objects.filter(object_set_id=self.pk).values("creator_id")[:5]
        return User.objects.filter(Q(id=self.creator.pk) | Q(id__in=[i['creator_id'] for i in users]))
    def count_object_set(self):
        count = Wall.objects.filter(object_set_id=self.pk).values("pk").count()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " человек "
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " человека "
        else:
            return str(count) + " людей "
    def get_first_object_set(self):
        return Wall.objects.filter(object_set_id=self.pk).first()

    def show_current_notify(self):
        if self.user_set:
            return self.get_user_set().first()
        elif self.post_set:
            return self.get_post_set().first()
        else:
            return self

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    @classmethod
    def u_notify_unread(cls, user_pk):
        cls.objects.filter(recipient_id=user_pk, status="U").update(status="R")

    @classmethod
    def c_notify_unread(cls, user_pk, community_id):
        cls.objects.filter(community_id=community_id, status="U").update(status="R")

    def is_unread(self):
        return self.status == "U"

    def get_notify(self, user):
        from common.attach.notify import get_notify
        return get_notify(user, self)

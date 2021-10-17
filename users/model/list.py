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


class UserFeaturedFriend(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    featured_user = models.PositiveIntegerField(default=0, verbose_name="Рекомендуемый друг")

    class Meta:
        verbose_name = 'Рекомендованные друзья'
        verbose_name_plural = 'Рекомендованные друзья'

class UserPopulateFriend(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    friend = models.PositiveIntegerField(default=0, verbose_name="Друг")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество визитов")

    class Meta:
        verbose_name = 'Популярность друзей'
        verbose_name_plural = 'Популярность друзей'
        ordering = ['-count']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.friend, self.count)

class UserPopulateCommunity(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    community = models.PositiveIntegerField(default=0, verbose_name="Сообщество")
    count = models.PositiveIntegerField(default=0, verbose_name="Количество визитов")

    class Meta:
        verbose_name = 'Популярность сообществ'
        verbose_name_plural = 'Популярность сообществ'
        ordering = ['-count']



class UserPhotoListPosition(models.Model):
    user = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")

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


class UserPostCanSeeWallIncludes(models.Model):
    """
        Таблица для ids пользователей, которые могут видеть стену пользователя с id owner.
        Выбирается в настройках приватности - "Некоторые друзья". Ниже все по аналогии
    """
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPostCanSeeWallExcludes(models.Model):
    """
        Таблица для ids пользователей, которые могут видеть стену пользователя с id owner.
        Выбирается в настройках приватности - "Все кроме". Ниже все по аналогии
    """
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPostCanSeeCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPostCanSeeCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPostAddItemIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPostAddItemExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPostAddCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPostAddCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class UserPhotoCanSeeGalleryIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPhotoCanSeeGalleryExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPhotoCanSeeCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPhotoCanSeeCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPhotoAddItemIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPhotoAddItemExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPhotoAddCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPhotoAddCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class UserGoodCanSeeMarketIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserGoodCanSeeMarketExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserGoodCanSeeCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserGoodCanSeeCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserGoodAddItemIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserGoodAddItemExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserGoodAddCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserGoodAddCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class UserVideoCanSeeVideoIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserVideoCanSeeVideoExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserVideoCanSeeCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserVideoCanSeeCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserVideoAddItemIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserVideoAddItemExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserVideoAddCommentIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserVideoAddCommentExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class UserMusicCanSeeMusicIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserMusicCanSeeMusicExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserMusicAddItemIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserMusicAddItemExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class UserPlannerCanSeeWorkspacesIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPlannerCanSeeWorkspacesExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPlannerCanSeeBoardsIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPlannerCanSeeBoardsExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPlannerCanSeeCardsIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPlannerCanSeeCardsExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPlannerCanSeeCommentsIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserPlannerCanSeeCommentsExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

class UserCommunityCanSeeIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserCommunityCanSeeExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

class UserFriendCanSeeIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserFriendCanSeeExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

class UserMessageCanSeeIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserMessageCanSeeExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

class UserDocCanSeeIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserDocCanSeeExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserDocAddIncludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class UserDocAddExcludes(models.Model):
    owner = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

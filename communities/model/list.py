from django.db import models


class CommunityPhotoListPosition(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения фотоальбома'
        verbose_name_plural = 'Порядки отображения фотоальбомов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class CommunityPostsListPosition(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка записей'
        verbose_name_plural = 'Порядки отображения списков записей'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class CommunityPlayListPosition(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения плейлиста'
        verbose_name_plural = 'Порядки отображения плейлистов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class CommunityGoodListPosition(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка товаров'
        verbose_name_plural = 'Порядки отображения списков товаров'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class CommunityVideoListPosition(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения видеольбома'
        verbose_name_plural = 'Порядки отображения видеоальбомов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class CommunitySurveyListPosition(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка опросов'
        verbose_name_plural = 'Порядки отображения списков опросов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)

class CommunityDocListPosition(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="Пользователь")
    list = models.PositiveIntegerField(default=0, verbose_name="Фотоальбом")
    position = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.PositiveSmallIntegerField(default=1, verbose_name="1 - открыт, 0 - недоступен")

    class Meta:
        verbose_name = 'Порядок отображения списка документов'
        verbose_name_plural = 'Порядки отображения списков документов'
        ordering = ['-position']

    def __str__(self):
        return '{} - {} :{}'.format(self.user, self.list, self.position)


class CommunityPostCanSeeWallIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPostCanSeeWallExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPostCanSeeCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPostCanSeeCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPostAddItemIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPostAddItemExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPostAddCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPostAddCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class CommunityPhotoCanSeeGalleryIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPhotoCanSeeGalleryExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPhotoCanSeeCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPhotoCanSeeCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPhotoAddItemIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPhotoAddItemExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPhotoAddCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPhotoAddCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class CommunityGoodCanSeeMarketIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityGoodCanSeeMarketExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityGoodCanSeeCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityGoodCanSeeCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityGoodAddItemIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityGoodAddItemExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityGoodAddCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityGoodAddCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class CommunityVideoCanSeeVideoIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityVideoCanSeeVideoExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityVideoCanSeeCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityVideoCanSeeCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityVideoAddItemIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityVideoAddItemExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityVideoAddCommentIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityVideoAddCommentExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class CommunityMusicCanSeeMusicIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityMusicCanSeeMusicExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityMusicAddItemIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityMusicAddItemExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")


class CommunityPlannerCanSeeWorkspacesIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPlannerCanSeeWorkspacesExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPlannerCanSeeBoardsIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPlannerCanSeeBoardsExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPlannerCanSeeCardsIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPlannerCanSeeCardsExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPlannerCanSeeCommentsIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityPlannerCanSeeCommentsExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

class CommunityMembersCanSeeIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityMembersCanSeeExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

class CommunityMessageCanSeeIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityMessageCanSeeExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

class CommunityDocCanSeeIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityDocCanSeeExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityDocAddIncludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")
class CommunityDocAddExcludes(models.Model):
    community = models.PositiveIntegerField(default=0, verbose_name="id назначателя")
    user = models.PositiveIntegerField(default=0, verbose_name="id пользователя")

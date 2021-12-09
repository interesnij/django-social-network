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

class CommunityDocsListPosition(models.Model):
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

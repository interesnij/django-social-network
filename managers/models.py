from django.db import models
from django.conf import settings
from django.db.models import Q


class UserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, blank=True, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в профиле'
        verbose_name_plural = 'Полномочия в профиле'

class CommunityStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_community_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в сообществе'
        verbose_name_plural = 'Полномочия в сообществе'

class PostUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в постах пользователей'
        verbose_name_plural = 'Полномочия в постах пользователей'

class PlannerUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='planner_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в планировщике'
        verbose_name_plural = 'Полномочия в планировщиках'

class ForumUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в форуме'
        verbose_name_plural = 'Полномочия в форуме'

class GoodUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='good_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в товарах пользователей'
        verbose_name_plural = 'Полномочия в товарах пользователей'

class DocUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в документах'
        verbose_name_plural = 'Полномочия в документах'

class PhotoUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в фотографиях'
        verbose_name_plural = 'Полномочия в фотографиях'

class VideoUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в видеозаписях'
        verbose_name_plural = 'Полномочия в видеозаписях'

class AudioUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='music_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в аудиозаписях'
        verbose_name_plural = 'Полномочия в аудиозаписях'

class SitesUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sites_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в сайтах'
        verbose_name_plural = 'Полномочия в сайтах'

class MailUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mail_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в почте'
        verbose_name_plural = 'Полномочия в почте'

class WikiUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wiki_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в википедии'
        verbose_name_plural = 'Полномочия в википедии'

class ArticleUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='article_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в статьях'
        verbose_name_plural = 'Полномочия в статьях'

class SurveyUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в опросах'
        verbose_name_plural = 'Полномочия в опросах'

class MessageUserStaff(models.Model):
    ADMINISTRATOR, EDITOR, ADVERTISER, MODERATOR = 1, 2, 3, 4
    LEVEL = ((ADMINISTRATOR, 'Администратор'),(MODERATOR, 'Модератор'),(EDITOR, 'Редактор'),(ADVERTISER, 'Рекламодатель'),)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_user_staff', verbose_name="Особый пользователь")
    level = models.PositiveSmallIntegerField(default=0, choices=LEVEL, verbose_name="Уровень доступа")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Полномочия в сообщениях'
        verbose_name_plural = 'Полномочия в сообщениях'

class CanWorkStaffUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_user', verbose_name="Создатель персонала")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей")
    can_work_support = models.BooleanField(default=False, verbose_name="Может добавлять техподдержку")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала'
        verbose_name_plural = 'Создатели персонала'

class CanWorkStaffCommunity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_community', verbose_name="Создатель персонала")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей")
    can_work_support = models.BooleanField(default=False, verbose_name="Может добавлять техподдержку")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала сообщетсв'
        verbose_name_plural = 'Создатели персонала сообщетсв'

class CanWorkStaffPostUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_post_user', verbose_name="Создатель персонала в записях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов записей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов записей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов записей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей записей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала записей'
        verbose_name_plural = 'Создатели персонала записей'

class CanWorkStaffGoodUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_good_user', verbose_name="Создатель персонала в товарах")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов товаров")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов товаров")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов товаров")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей товаров")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала товаров'
        verbose_name_plural = 'Создатели персонала товаров'

class CanWorkStaffDocUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_doc_user', verbose_name="Создатель персонала в товарах")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов докуметов")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов докуметов")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов докуметов")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей докуметов")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала докуметов'
        verbose_name_plural = 'Создатели персонала докуметов'

class CanWorkStaffPhotoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_photo_user', verbose_name="Создатель персонала в фотографиях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов фотографий")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов фотографий")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов фотографий")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей фотографий")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала фотографий'
        verbose_name_plural = 'Создатели персонала фотографий'

class CanWorkStaffVideoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_video_user', verbose_name="Создатель персонала в видеозаписях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов видеозаписей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов видеозаписей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов видеозаписей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей видеозаписей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала видеозаписей'
        verbose_name_plural = 'Создатели персонала видеозаписей'

class CanWorkStaffAudioUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_audio_user', verbose_name="Создатель персонала в аудиозаписях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов аудиозаписей")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов аудиозаписей")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов аудиозаписей")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей аудиозаписей")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала аудиозаписей'
        verbose_name_plural = 'Создатели персонала аудиозаписей'

class CanWorkStaffPlannerUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_planner_user', verbose_name="Создатель персонала в планировщике")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в планировщике")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в планировщике")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в планировщике")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в планировщике")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в планировщике'
        verbose_name_plural = 'Создатели персонала в планировщике'

class CanWorkStaffForumUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_forum_user', verbose_name="Создатель персонала в форуме")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в форуме")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в форуме")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в форуме")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в форуме")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в форуме'
        verbose_name_plural = 'Создатели персонала в форуме'

class CanWorkStaffMailUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_mail_user', verbose_name="Создатель персонала в почте")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в почте")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в почте")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в почте")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в почте")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в почте'
        verbose_name_plural = 'Создатели персонала в почте'

class CanWorkStaffSitesUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_sites_user', verbose_name="Создатель персонала в сайтах")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в сайтах")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в сайтах")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в сайтах")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в сайтах")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в сайтах'
        verbose_name_plural = 'Создатели персонала в сайтах'

class CanWorkStaffWikiUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_wiki_user', verbose_name="Создатель персонала в википедии")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в википедии")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в википедии")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в википедии")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в википедии")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в википедии'
        verbose_name_plural = 'Создатели персонала в википедии'

class CanWorkStaffArticleUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_article_user', verbose_name="Создатель персонала в статьях")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в статьях")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в статьях")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в статьях")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в статьях")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в статьях'
        verbose_name_plural = 'Создатели персонала в статьях'

class CanWorkStaffSurveyUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_survey_user', verbose_name="Создатель персонала в опросах")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в опросах")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в опросах")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в опросах")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в опросах")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в опросах'
        verbose_name_plural = 'Создатели персонала в опросах'

class CanWorkStaffMessageUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='can_work_staff_message_user', verbose_name="Создатель персонала в опросах")
    can_work_administrator = models.BooleanField(default=False, verbose_name="Может добавлять администраторов в сообщениях")
    can_work_moderator = models.BooleanField(default=False, verbose_name="Может добавлять модераторов в сообщениях")
    can_work_editor = models.BooleanField(default=False, verbose_name="Может добавлять редакторов в сообщениях")
    can_work_advertiser = models.BooleanField(default=False, verbose_name="Может добавлять рекламодателей в сообщениях")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'Создатель персонала в сообщениях'
        verbose_name_plural = 'Создатели персонала в сообщениях'

USER, COMMUNITY, SITE = 1,2,6
POST_LIST, POST, POST_COMMENT = 8, 9, 10
PHOTO_LIST, PHOTO, PHOTO_COMMENT = 12, 13, 14
DOC_LIST, DOC = 17, 18
SURVEY_LIST, SURVEY = 21, 22
MUSIC_LIST, MUSIC = 25, 26
VIDEO_LIST, VIDEO, VIDEO_COMMENT = 29, 30, 31
GOOD_LIST, GOOD, GOOD_COMMENT = 33, 34, 35
WORKSPACE, BOARD, COLUMN, CARD, CARD_COMMENT = 38, 39, 40, 41, 42
FORUM_ITEM, FORUM_COMMENT = 45, 46
MAIL, MESSAGE, WIKI = 54, 55, 56
ARTICLE_LIST, ARTICLE = 58, 59

TYPE = (
    (USER, 'Пользователь'),(COMMUNITY, 'Сообщество'),(SITE, 'Сайт'),(ARTICLE, 'Статья'),(ARTICLE_LIST, 'Список статей'),
    (MUSIC_LIST, 'Плейлист'),(MUSIC, 'Трек'),
    (POST_LIST, 'Список записей'),(POST, 'Запись'),(POST_COMMENT, 'Коммент к записи'),
    (DOC_LIST, 'Список документов'),(DOC, 'Документ'),
    (SURVEY_LIST, 'Список опросов'),(SURVEY, 'Опрос'),
    (PHOTO_LIST, 'Список фотографий'),(PHOTO, 'Фотография'),(PHOTO_COMMENT, 'Коммент к фотографии'),
    (VIDEO_LIST, 'Список роликов'),(VIDEO, 'Ролик'), (VIDEO_COMMENT, 'Коммент к ролику'),
    (GOOD_LIST, 'Список товаров'),(GOOD, 'Товар'),(GOOD_COMMENT, 'Коммент к товару'),
    (WORKSPACE, 'Рабочее пространство'),(BOARD, 'Доска'),(COLUMN, 'Колонка'),(CARD, 'Карточка'),(CARD_COMMENT, 'Коммент к карточке'),
    (FORUM_ITEM, 'Обсуждение'),(FORUM_COMMENT, 'Коммент к обсуждению'),
    (MAIL, 'Почта'),(MESSAGE, 'Сообщения'), (WIKI, 'Объект википедии')
)


class Moderated(models.Model):
    # рассмотрение жалобы на объект, получаемфй по attach. Применение санкций или отвергание жалобы. При применении удаление жалоб-репортов
    PENDING, SUSPEND, CLOSE, BANNER_GET, REJECTED = 1, 2, 3, 4, 5
    STATUS = (
        (PENDING, 'На рассмотрении'),
        (SUSPEND, 'Объект заморожен'),
        (CLOSE, 'Объект закрыт'),
        (BANNER_GET, 'Объекту присвоен баннер'),
        (REJECTED, 'Отвергнутый'),
    )
    description = models.TextField(max_length=300, blank=True, verbose_name="Описание")
    verified = models.BooleanField(default=False, verbose_name="Проверено")
    status = models.PositiveSmallIntegerField(choices=STATUS, default=PENDING, verbose_name="Статус")
    type = models.PositiveSmallIntegerField(default=0, choices=TYPE, verbose_name="Класс объекта")
    object_id = models.PositiveIntegerField(default=0, verbose_name="id объекта")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Проверяемый объект'
        verbose_name_plural = 'Проверяемые объект'

    @classmethod
    def create_moderated_object(cls, type, object_id):
        return cls.objects.create(type=type, object_id=object_id)

    @classmethod
    def _get_or_create_moderated_object(cls, type, object_id):
        try:
            moderated_object = cls.objects.get(type=type, object_id=object_id)
            moderated_object.verified = False
            moderated_object.save(update_fields=['verified'])
        except cls.DoesNotExist:
            moderated_object = cls.create_moderated_object(type=type, object_id=object_id)
        return moderated_object

    @classmethod
    def get_or_create_moderated_object(cls, type, object_id):
        return cls._get_or_create_moderated_object(type=type, object_id=object_id)

    def reports_count(self):
        # кол-во жалоб на пользователя
        return self.reports.count()

    def reports_count_ru(self):
        count = self.reports_count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " жалоба"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " жалобы"
        else:
            return str(count) + " жалоб"

    def is_verified(self):
        # проверен ли пользователь
        return self.verified
    def is_suspend(self):
        # Объект заморожен
        return self.status == Moderated.SUSPEND
    def is_pending(self):
        # Жалоба рассматривается
        return self.status == Moderated.PENDING
    def is_bloked(self):
        # Объект блокирован
        return self.status == Moderated.BLOCKED
    def is_banner(self):
        # Объект блокирован
        return self.status == Moderated.BANNER_GET

    def create_suspend(self, manager_id, duration_of_penalty):
        self.verified = True
        ModerationPenalty.create_suspension_penalty(moderated_object=self, manager_id=manager_id, type=self.type, object_id=self.object_id, expiration=duration_of_penalty)
        self.save()
    def create_warning_banner(self, manager_id):
        self.verified = True
        self.save()
        ModerationPenalty.create_banner_penalty(moderated_object=self, manager_id=manager_id, type=self.type, object_id=self.object_id)
    def create_close(self, object, description, manager_id):
        self.status = Moderated.CLOSE
        self.description = description
        self.verified = True
        self.save()
        ModerationPenalty.create_close_penalty(moderated_object=self, manager_id=manager_id, type=self.type, object_id=self.object_id)
        if self.type < 5:
            object.close_item()
        elif object.community:
            object.close_item(object.community)
        else:
            object.close_item(None)
    def delete_close(self, object, manager_id):
        obj = ModerationPenalty.objects.get(moderated_object=self, type=self.type, object_id=self.object_id)
        obj.delete()
        if self.type < 5:
            object.abort_close_item()
        elif object.community:
            object.abort_close_item(object.community)
        else:
            object.abort_close_item(None)
        self.delete()
    def delete_suspend(self, manager_id):
        obj = ModerationPenalty.objects.get(moderated_object=self, type=self.type, object_id=self.object_id)
        obj.delete()
        self.delete()
    def delete_warning_banner(self, manager_id):
        obj = ModerationPenalty.objects.get(moderated_object=self, type=self.type, object_id=self.object_id)
        obj.delete()
        self.delete()

    def unverify_moderation(self, object, manager_id):
        self.verified = False
        self.moderated_object.all().delete()
        if self.type == 1:
            from users.models import User
            user = User.objects.get(pk=self.object_id)
            user.abort_close_item()
            user.abort_suspend_item()
        elif self.type == 2:
            from communities.models import Community
            community = Community.objects.get(pk=self.object_id)
            community.abort_close_item()
            community.abort_suspend_item()
        elif self.type < 5:
            object.abort_close_item(None)
        elif object.community:
            object.abort_close_item(object.community)
        else:
            object.abort_close_item(None)
        self.save()

    def reject_moderation(self, manager_id):
        self.verified = True
        self.status = Moderated.REJECTED
        self.save()

    def get_reports(self):
        return self.reports.all()

    def get_btn_console(self):
        return '<div class="border-top btn_console"><a class="create_user_suspend pointer">Заморозить</a>| <a class="create_user_close pointer">Заблокировать</a>| <a class="create_user_warning_banner pointer">Повесить баннер</a>| <a class="create_user_rejected pointer">Отклонить</a></div>'

    def get_user(self):
        try:
            from users.models import User
            user = User.objects.get(pk=self.object_id)
            return ''.join(['<div class="media"><a href="/users/', str(self.object_id), '" class="ajax"><figure><img src="', user.get_avatar(), \
            '" style="width: 90px;" alt="image"></figure></a><div class="media-body pl-1"><h6 class="my-0 mt-1"><a href="/users/', \
            str(self.object_id), '" class="ajax"><h6 class="mt-1">', user.get_full_name(), '</h6></a><span class="mt-1 pointer underline show_object_reports" obj-pk="', str(self.pk), '">', self.reports_count_ru(), \
            '</span><div class="border mt-1 btn_console" data-pk="', str(self.object_id), '"><a class="create_user_suspend pointer">Заморозить</a> | <a class="create_user_close pointer">Заблокировать</a> | <a class="create_user_warning_banner pointer">Повесить баннер</a> | <a class="create_user_rejected pointer">Отклонить</a></div></div></div>'])
        except:
            return '<div class="media">Ошибка отображения данных</div>'

    def get_blog(self, user):
        #try:
        from blog.models import Blog
        blog = Blog.objects.get(pk=self.object_id)
        creator = blog.creator
        return ''.join(['<div class="d-flex justify-content-start align-items-center mb-1"><div class="avatar mr-1"><a href="/blog/', str(blog.slug), '/" class="ajax"><img src="', blog.get_image(), '" alt="avatar img" height="40" width="40"></a></div><div class="profile-user-info"><a href="/blog/', str(blog.slug), '/" class="ajax"><h4 class="mb-0">', blog.title, ' <span class="text-muted small">(', blog.get_created(), ')</span></h4></a><span class="small"><a href="/users/', str(creator.pk), '">', creator.get_full_name(),'</a></span></div></div><p class="card-text mb-50">', blog.description, '</p><span><span><span><span class="small" data-pk="', str(blog.pk), '"><span class="create_blog_close pointer underline">Заблокировать</span>&nbsp;&nbsp;<span class="create_blog_rejected pointer underline">Отклонить</span></span></span></span></span>'])
        #except:
        #    return ''
    def get_blog_comment(self, user):
        try:
            from common.model.comments import BlogComment
            comment = BlogComment.objects.get(pk=self.object_id)
            creator = comment.commenter
            if comment.attach:
                _attach = comment.get_u_attach(user)
            else:
                _attach = ''
            return ''.join(['<div class="card-body" style="padding: .5rem .5rem;"><div class="media"><div class="avatar mr-75"><a href="/users/', str(creator.pk), '/" class="ajax"><img src="', creator.get_avatar(), '" width="38" height="38" alt="Avatar"></a></div><div class="media-body"><h6 class="font-weight-bolder mb-25"><a href="/users/', str(creator.pk), '/" class="ajax">', creator.get_full_name(), '</a></h6><span class="text-muted small">', comment.get_created(), '</span><br></div></div><div class="comment_footer"><span class="card-text">', comment.text, '</span>', _attach, ' <span><div class="border mt-1 btn_console" data-pk="', str(comment.pk), '"><a " obj-pk="', str(self.pk), '" class="show_object_reports pointer">', self.reports_count_ru(), '</a> | <a class="create_blog_comment_close pointer">Закрыть</a> | <a class="create_blog_comment_rejected pointer">Отклонить</a></div></span></div></div>'])
        except:
            return ''

    def get_photo(self):
        try:
            from gallery.models import Photo
            photo = Photo.objects.get(pk=self.object_id)
            return ''.join(['<div class="uuid_keeper" data-uuid="', str(photo.uuid), '"><div class="progressive replace image_fit_200 u_photo_moderated_detail pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
        except:
            return ''
    def get_video(self):
        try:
            from video.models import Video
            video = Video.objects.get(pk=self.object_id)
            return ''.join(['<div><img class="image_fit uuid_keeper" data-uuid="', str(video.uuid), '" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_video_moderated_detail" video-pk="', str(video.pk), '"></div></div>'])
        except:
            return ''
    def get_doc(self):
        try:
            from docs.models import Doc
            doc = Doc.objects.get(pk=self.object_id)
            options = '<span class="dropdown-item create_doc_close">Заблокировать</span><span class="dropdown-item create_doc_rejected">Отклонить</span>'
            opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg class="svg_info" style="padding-top: 3px;" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 33px;">' + options + '<span class="dropdown-item show_object_reports" obj-pk="' + str(self.pk) + '">' + self.reports_count_ru() + '</span></div></div>'
            span_btn = ''.join(['<span class="span_btn">', opt_drop, '</span>'])
            return ''.join(['<div style="flex-basis: 100%;"><div class="media border"><svg fill="currentColor" class="svg_default" style="width:45px;margin: 0;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg><div class="media-body doc_media_body"><h6 class="pointer" style="padding-top: 5px;width: 84%;overflow: hidden;"><a href="', doc.file.url, '" target="_blank" rel="nofollow">', doc.title, '</a></h6><span class="small" style="position: absolute;">', str(doc.file.size), ' | ', doc.get_mime_type(), '</span>', span_btn, '</div></div></div>'])
        except:
            return ''

    def get_music(self):
        try:
            from music.models import Music
            music = Music.objects.get(pk=self.object_id)
            options = '<span class="dropdown-item create_track_close">Заблокировать</span><span class="dropdown-item create_track_rejected">Отклонить</span>'
            opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg style="width: 17px;padding-top:3px" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 55px;">' + options + '<span class="dropdown-item show_object_reports" obj-pk="' + str(self.pk) + '">' + self.reports_count_ru() + '</span></div></div>'
            span_btn = ''.join(['<span class="span_btn">', opt_drop, '</span>'])
            return ''.join(['<div class="col-md-12" style="flex-basis: 100%;"><div class="media border p-1"><div class="media-body music_media_body" style="line-height: 8px;"><span>', music.title, '</span><div class="audio_div"><audio id="player" class="audio_player"><source src="', music.get_uri(), '" type="audio/mp3" /></audio></div>', span_btn, '</div></div></div>'])
        except:
            return ''

    def get_photo_list(self):
        try:
            from gallery.models import PhotoList
            list = PhotoList.objects.get(pk=self.object_id)
            creator = list.creator
            add = ''
            return ''.join(['<div style="width: 100%;height: 100%;" class="text-center bg-dark position-relative uuid_keeper" data-uuid="', str(list.uuid), '"  photolist-pk="', str(self.object_id), '"><figure class="background-img"><img src="', list.get_cover_photo(), '">"</figure><div class="container pt-2"><h4 class="u_load_moderated_photo_list text-white pointer"><a class="nowrap">', list.name, '</a></h4><p class="show_object_reports">Жалоб: ', str(self.reports_count()), '</p><hr class="my-4"><a class="u_load_moderated_photo_list text-white pointer">', list.count_items_ru(), '</a><div class="row">', add, '</div>', '</div></div>'])
        except:
            return ''
    def get_doc_list(self):
        try:
            from docs.models import DocsList
            list = DocsList.objects.get(pk=self.object_id)
            creator = list.creator
            image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;"><div class="card-body border uuid_keeper" data-uuid="', str(list.uuid), '"  doclist-pk="', str(list.pk), '" style="padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_moderated_doc_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_moderated_doc_list pointer">', list.name, '</h6><p class="show_object_reports">Жалоб: ', str(self.reports_count()), '">', str(creator.get_full_name_genitive()), '</a><br><span class="show_object_reports pointer">Жалоб: ', str(self.reports_count()), '</span></p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''
    def get_video_list(self):
        try:
            from video.models import VideoList
            list = VideoList.objects.get(pk=self.object_id)
            creator = list.creator
            image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;" class="card border"><div class="card-body uuid_keeper" data-uuid="', str(list.uuid), '"  videolist-pk="', str(creator.pk), '" style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_moderated_video_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_moderated_video_list pointer">', list.name, '</h6><p>Список видеозаписей <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br><span class="show_object_reports pointer">Жалоб: ', str(self.reports_count()), '</span></p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''
    def get_playlist(self):
        try:
            from music.models import MusicList
            playlist = MusicList.objects.get(pk=self.object_id)
            creator = playlist.creator
            image = '<svg fill="currentColor" class="svg_default" style="width:70px;height:70px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;" class="border"><div class="card-body uuid_keeper" data-uuid="', str(playlist.uuid), '" playlist-pk="', str(playlist.pk), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_moderated_playlist pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_moderated_playlist pointer">', playlist.name, '</h6><p>Плейлист <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br><span class="show_object_reports pointer">Жалоб: ', str(self.reports_count()), '</span></p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''
    def get_survey_list(self):
        try:
            from survey.models import SurveyList
            list = SurveyList.objects.get(pk=self.object_id)
            creator = list.creator
            image = '<svg height="70px" viewBox="0 0 24 24" width="70px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"></path><path d="M18 9l-1.41-1.42L10 14.17l-2.59-2.58L6 13l4 4zm1-6h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-.14 0-.27.01-.4.04-.39.08-.74.28-1.01.55-.18.18-.33.4-.43.64-.1.23-.16.49-.16.77v14c0 .27.06.54.16.78s.25.45.43.64c.27.27.62.47 1.01.55.13.02.26.03.4.03h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7-.25c.41 0 .75.34.75.75s-.34.75-.75.75-.75-.34-.75-.75.34-.75.75-.75zM19 19H5V5h14v14z"></path></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;" class="border"><div class="card-body uuid_keeper" data-uuid="', str(list.uuid), '" surveylist-pk="', str(list.pk), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_moderated_survey_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_moderated_survey_list pointer">', list.name, '</h6><p>Список опросов <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br><span class="show_object_reports pointer">Жалоб: ', str(self.reports_count()), '</span></p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''

    def get_doc_items(self):
        if self.type == 17:
            return self.get_doc_list()
        elif self.type == 18:
            return self.get_doc()
    def get_survey_items(self):
        if self.type == 21:
            return self.get_survey_list()
        elif self.type == 22:
            return self.get_survey()
    def get_photo_items(self):
        if self.type == 12:
            return self.get_photo_list()
        elif self.type == 13:
            return self.get_photo()
    def get_video_items(self):
        if self.type == 29:
            return self.get_video_list()
        elif self.type == 30:
            return self.get_video()
    def get_music_items(self):
        if self.type == 25:
            return self.get_playlist()
        elif self.type == 26:
            return self.get_music()

    @classmethod
    def get_moderation_users(cls):
        return cls.objects.filter(type=1, verified=False)
    @classmethod
    def get_moderation_communities(cls):
        return cls.objects.filter(type=2, verified=False)
    @classmethod
    def get_moderation_photos(cls):
        types = Q(verified=False,type__gt=11)&Q(type__lt=15)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_videos(cls):
        types = Q(verified=False,type__gt=28)&Q(type__lt=32)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_audios(cls):
        types = Q(verified=False,type__gt=24)&Q(type__lt=27)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_survey(cls):
        types = Q(verified=False,type__gt=20)&Q(type__lt=23)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_docs(cls):
        types = Q(verified=False,type__gt=16)&Q(type__lt=19)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_sites(cls):
        return cls.objects.filter(type=6,verified=False)
    @classmethod
    def get_moderation_articles(cls):
        return cls.objects.filter(type=7,verified=False)
    @classmethod
    def get_moderation_goods(cls):
        types = Q(verified=False,type__gt=32)&Q(type__lt=36)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_planner(cls):
        types = Q(verified=False,type__gt=37)&Q(type__lt=43)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_forum(cls):
        types = Q(verified=False,type__gt=44)&Q(type__lt=47)
        return cls.objects.filter(types)
    @classmethod
    def get_moderation_wiki(cls):
        types = Q(verified=False,type__gt=48)&Q(type__lt=51)
        return cls.objects.filter(types)


class ModerationReport(models.Model):
    # жалобы на объект.
    PORNO = 'P'
    NO_CHILD = 'NC'
    SPAM = 'S'
    BROKEN = 'B'
    FRAUD = 'F'
    CLON = 'K'
    OLD_PAGE = 'OP'
    DRUGS = 'D'
    NO_MORALITY = 'NM'
    RHETORIC_HATE = "RH"
    UNETHICAL = "U"
    TYPE = (
        (PORNO, 'Порнография'),
        (NO_CHILD, 'Для взрослых'),
        (SPAM, 'Рассылка спама'),
        (BROKEN, 'Оскорбительное поведение'),
        (FRAUD, 'Мошенничество'),
        (CLON, 'Клон моей страницы'),
        (OLD_PAGE, 'Моя старая страница'),
        (DRUGS, 'Наркотики'),
        (NO_MORALITY, 'Не нравственный контент'),
        (RHETORIC_HATE, 'Риторика ненависти'),
        (UNETHICAL, 'Неэтичное поведение'),
    )

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reporter', null=False, verbose_name="Репортер")
    moderated_object = models.ForeignKey(Moderated, on_delete=models.CASCADE, related_name='reports', null=False, verbose_name="Объект")
    description = models.CharField(max_length=300, blank=True, verbose_name="Описание")
    type = models.PositiveSmallIntegerField(default=0, choices=TYPE, verbose_name="Класс объекта")

    def __str__(self):
        return self.reporter.get_full_name()

    class Meta:
        verbose_name = 'Жалоба на объект'
        verbose_name_plural = 'Жалобы на объект'

    @classmethod
    def create_moderation_report(cls, reporter_id, _type, object_id, description, type):
        moderated_object = Moderated.get_or_create_moderated_object(type=_type, object_id=object_id)
        return cls.objects.create(reporter_id=reporter_id, type=type, description=description, moderated_object=moderated_object)

    @classmethod
    def is_user_already_reported(cls, reporter_id, type, object_id):
        return cls.objects.filter(reporter_id=reporter_id, type=type, moderated_object_id=object_id).exists()


class ModerationPenalty(models.Model):
    # сами санкции против объекта.
    SUSPENSION, CLOSE, BANNER = 1,2,3
    STATUS = ((SUSPENSION, 'Приостановлено'), (CLOSE, 'Закрыто'), (BANNER, 'Вывешен баннер'),)

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='manager_penalties', verbose_name="Менеджер")
    expiration = models.DateTimeField(null=True, blank=True, verbose_name="Окончание")
    moderated_object = models.ForeignKey(Moderated, on_delete=models.CASCADE, related_name='moderated_object', verbose_name="Объект")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Класс объекта")
    object_id = models.PositiveIntegerField(default=0, verbose_name="id объекта")
    status = models.PositiveSmallIntegerField(default=0, choices=STATUS, verbose_name="Статус объекта")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Оштрафованный объект'
        verbose_name_plural = 'Оштрафованные объект'

    @classmethod
    def create_suspension_penalty(cls, object_id, type, manager_id, moderated_object, expiration):
        try:
            obj = cls.objects.get(moderated_object=moderated_object)
            obj.delete()
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.SUSPENSION, expiration=expiration)
        except:
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.SUSPENSION, expiration=expiration)
    @classmethod
    def create_close_penalty(cls, object_id, type, manager_id, moderated_object):
        try:
            obj = cls.objects.get(moderated_object=moderated_object)
            obj.delete()
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.CLOSE)
        except:
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.CLOSE)
    @classmethod
    def create_banner_penalty(cls, object_id, type, manager_id, moderated_object):
        try:
            obj = cls.objects.get(moderated_object=moderated_object)
            obj.delete()
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.BANNER)
        except:
            return cls.objects.create(moderated_object=moderated_object, manager_id=manager_id, object_id=object_id, type=type, status=cls.BANNER)

    def is_suspend(self):
        # Объект заморожен
        return self.status == ModerationPenalty.SUSPENSION
    def is_closed(self):
        # Объект блокирован
        return self.status == ModerationPenalty.CLOSE
    def is_banner(self):
        # Объект блокирован
        return self.status == ModerationPenalty.BANNER

    @classmethod
    def get_penalty_blog(cls, user_id):
        return cls.objects.filter(manager__id=user_id, type__contains="BL")

    def get_user(self):
        try:
            from users.models import User
            user = User.objects.get(pk=self.object_id)
            if self.is_suspend():
                span = '<span class="small">До ' + str(self.expiration) + '</span> (<a class="small remove_user_suspend pointer">Отменить заморозку</a> | <a class="small user_unverify pointer">Отменить проверку</a>)'
            elif self.is_closed():
                span = '<span class="small">Заблокирован</span> (<a class="small remove_user_close pointer">Отменить блокировку</a> | <a class="small user_unverify pointer">Отменить проверку</a>)'
            elif self.is_banner():
                span = '<span class="small">Баннер предупреждения</span> (<a class="small remove_user_warning_banner pointer">Убрать баннер</a> | <a class="small user_unverify pointer">Отменить проверку</a>)'
            else:
                span = '<span class="small">Санкции не применены</span>'
            return ''.join(['<div class="media"><a href="/users/', str(self.object_id), '" class="ajax"><figure><img src="', user.get_avatar(), \
            '" style="width: 90px;" alt="image"></figure></a><div class="media-body pl-1"><h6 class="my-0 mt-1"><a href="/users/', \
            str(self.object_id), '" class="ajax"><h6 class="mt-1">', user.get_full_name(), \
            '</h6></a></h6><div class=""></div><div class="border-top btn_console" user-pk="', str(self.object_id), '">', span, '</div></div></div>'])
        except:
            return '<div class="media">Ошибка отображения данных</div>'

    def get_photo(self):
        try:
            from gallery.models import Photo
            photo = Photo.objects.get(pk=self.object_id)
            return ''.join(['<div class="uuid_keeper" data-uuid="', str(photo.uuid), '"><div class="progressive replace image_fit_200 penalty_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
        except:
            return ''
    def get_video(self):
        try:
            from video.models import Video
            video = Video.objects.get(pk=self.object_id)
            return ''.join(['<div class="video" data-uuid="', str(video.get_list_uuid()), '"><img class="image_fit uuid_keeper" data-uuid="', str(video.uuid), '" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_video_penalty_detail" video-pk="', str(video.pk), '"></div></div>'])
        except:
            return ''
    def get_blog_comment(self, user):
        try:
            from common.model.comments import BlogComment
            comment = BlogComment.objects.get(pk=self.object_id)
            creator = comment.commenter
            if comment.attach:
                _attach = comment.get_u_attach(user)
            else:
                _attach = ''
            return ''.join(['<div class="card-body" style="padding: .5rem .5rem;"><div class="media"><div class="avatar mr-75"><a href="/users/', str(creator.pk), '/" class="ajax"><img src="', creator.get_avatar(), '" width="38" height="38" alt="Avatar"></a></div><div class="media-body"><h6 class="font-weight-bolder mb-25"><a href="/users/', str(creator.pk), '/" class="ajax">', creator.get_full_name(), '</a></h6><span class="text-muted small">', comment.get_created(), '</span><br></div></div><div class="comment_footer"><span class="card-text">', comment.text, '</span>', _attach, ' <div class="border mt-1 btn_console" data-pk="', str(comment.pk), '"><a class="remove_blog_comment_close pointer">Восстановить</a> | <a class="blog_comment_unverify pointer">Отменить проверку</a></div></div></div>'])
        except:
            return ''
    def get_doc(self):
        try:
            from docs.models import Doc
            doc = Doc.objects.get(pk=self.object_id)
            span_btn, status = '', ''
            if doc.is_closed():
                status = '<span class="small">Заблокировано</span>'
                options = '<span class="dropdown-item remove_doc_close">Разблокировать</span><span class="dropdown-item doc_unverify">Отменить проверку</span>'
            opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg class="svg_info" style="padding-top: 3px;" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 33px;">' + options + '</div></div>'
            span_btn = ''.join([span_btn, '<span class="span_btn">', opt_drop, '</span>'])
            return ''.join(['<div class="photo" style="flex-basis: 100%;"><div class="media border"><svg fill="currentColor" class="svg_default" style="width:45px;margin: 0;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg><div class="media-body doc_media_body"><h6 class="pointer" style="padding-top: 5px;width: 84%;overflow: hidden;"><a href="', doc.file.url, '" target="_blank" rel="nofollow">', doc.title, ' (', status, ')</a></h6><span class="small" style="position: absolute;">', str(doc.file.size), ' | ', doc.get_mime_type(), '</span>', span_btn, '</div></div></div>'])
        except:
            return ''

    def get_music(self):
        try:
            from music.models import Music
            music = Music.objects.get(pk=self.object_id)
            span_btn, status = '', ''
            if music.is_closed():
                status = '<span class="small">Заблокировано</span>'
                options = '<span class="dropdown-item remove_track_close">Разблокировать</span><span class="dropdown-item track_unverify">Отменить проверку</span>'
            opt_drop = '<div class="dropdown" style="position: inherit;"><a class="btn_default drop pointer"><svg style="width: 17px;padding-top:3px" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"></path></svg></a><div class="dropdown-menu dropdown-menu-right" style="top: 55px;">' + options + '</div></div>'
            span_btn = ''.join([span_btn, '<span class="span_btn">', opt_drop, '</span>'])
            return ''.join(['<div class="col-md-12" style="flex-basis: 100%;"><div class="media border p-1"><div class="media-body music_media_body" style="line-height: 8px;"><span>', music.title, ' (', status, ')</span><div class="audio_div"><audio id="player" class="audio_player"><source src="', music.get_uri(), '" type="audio/mp3" /></audio></div>', span_btn, '</div></div></div>'])
        except:
            return ''

    def get_photo_list(self):
        try:
            from gallery.models import PhotoList
            list = PhotoList.objects.get(pk=self.object_id)
            creator = list.creator
            add = ''
            return ''.join(['<div style="width: 100%;height: 100%;" class="text-center bg-dark position-relative uuid_keeper" data-uuid="', str(list.uuid), '"  photolist-pk="', str(self.object_id), '"><figure class="background-img"><img src="', list.get_cover_photo(), '">"</figure><div class="container pt-2"><h4 class="u_load_penalty_photo_list text-white pointer"><a class="nowrap">', list.name, '</a></h4><p><a class="ajax underline text-white nowrap" href="/users/', str(creator.pk), '">', str(creator), '</a></p><hr class="my-4"><a class="u_load_penalty_photo_list text-white pointer">', list.count_items_ru(), '</a><div class="row">', add, '</div>', '</div></div>'])
        except:
            return ''
    def get_doc_list(self):
        try:
            from docs.models import DocsList
            list = DocsList.objects.get(pk=self.object_id)
            creator = list.creator
            image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;"><div class="card-body border uuid_keeper" data-uuid="', str(list.uuid), '"  doclist-pk="', str(list.pk), '" style="padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_penalty_doc_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_penalty_doc_list pointer">', list.name, '</h6><p>Список документов <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Документов: ', str(list.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''
    def get_video_list(self):
        try:
            from video.models import VideoList
            list = VideoList.objects.get(pk=self.object_id)
            creator = list.creator
            image = '<svg fill="currentColor" class="svg_default" style="width:60px;height:88px;" viewBox="0 0 24 24"><path d="M18 3v2h-2V3H8v2H6V3H4v18h2v-2h2v2h8v-2h2v2h2V3h-2zM8 17H6v-2h2v2zm0-4H6v-2h2v2zm0-4H6V7h2v2zm10 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"></path></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;" class="card border"><div class="card-body uuid_keeper" data-uuid="', str(list.uuid), '"  videolist-pk="', str(creator.pk), '" style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_penalty_video_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_penalty_video_list pointer">', list.name, '</h6><p>Список видеозаписей <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Видеозаписей: ', str(list.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''
    def get_playlist(self):
        try:
            from music.models import MusicList
            playlist = MusicList.objects.get(pk=self.object_id)
            creator = playlist.creator
            image = '<svg fill="currentColor" class="svg_default" style="width:70px;height:70px;" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M15 6H3v2h12V6zm0 4H3v2h12v-2zM3 16h8v-2H3v2zM17 6v8.18c-.31-.11-.65-.18-1-.18-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3V8h3V6h-5z"/></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;" class="border"><div class="card-body uuid_keeper" data-uuid="', str(playlist.uuid), '" playlist-pk="', str(playlist.pk), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_penalty_playlist pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_penalty_playlist pointer">', playlist.name, '</h6><p>Плейлист <a class="ajax underline" href="/  users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Треков: ', str(playlist.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''
    def get_survey_list(self):
        try:
            from survey.models import SurveyList
            list = SurveyList.objects.get(pk=self.object_id)
            creator = list.creator
            image = '<svg height="70px" viewBox="0 0 24 24" width="70px" fill="currentColor"><path d="M0 0h24v24H0V0z" fill="none"></path><path d="M18 9l-1.41-1.42L10 14.17l-2.59-2.58L6 13l4 4zm1-6h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-.14 0-.27.01-.4.04-.39.08-.74.28-1.01.55-.18.18-.33.4-.43.64-.1.23-.16.49-.16.77v14c0 .27.06.54.16.78s.25.45.43.64c.27.27.62.47 1.01.55.13.02.26.03.4.03h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7-.25c.41 0 .75.34.75.75s-.34.75-.75.75-.75-.34-.75-.75.34-.75.75-.75zM19 19H5V5h14v14z"></path></svg>'
            add_svg = ''
            return ''.join(['<div style="flex-basis: 100%;" class="border"><div class="card-body uuid_keeper" data-uuid="', str(list.uuid), '" surveylist-pk="', str(list.pk), '"style="padding: 8px;padding-bottom: 0;"><div style="display:flex"><figure><a class="u_load_penalty_survey_list pointer">', image, '</a></figure><div class="media-body" style="margin-left: 10px;"><h6 class="my-0 mt-1 u_load_penalty_survey_list pointer">', list.name, '</h6><p>Список опросов <a class="ajax underline" href="/users/', str(creator.pk), '">', str(creator.get_full_name_genitive()), '</a><br>Треков: ', str(list.count_items()), '</p></div><span class="list_share">', add_svg, '</span></div></div></div>'])
        except:
            return ''

    def get_doc_items(self):
        if self.type == 17:
            return self.get_doc_list()
        elif self.type == 18:
            return self.get_doc()
    def get_survey_items(self):
        if self.type == 21:
            return self.get_survey_list()
        elif self.type == 22:
            return self.get_survey()
    def get_photo_items(self):
        if self.type == 12:
            return self.get_photo_list()
        elif self.type == 13:
            return self.get_photo()
    def get_video_items(self):
        if self.type == 29:
            return self.get_video_list()
        elif self.type == 30:
            return self.get_video()
    def get_music_items(self):
        if self.type == 25:
            return self.get_playlist()
        elif self.type == 26:
            return self.get_music()

    @classmethod
    def get_penalty_users(cls):
        return cls.objects.filter(type=1, verified=False)
    @classmethod
    def get_penalty_communities(cls):
        return cls.objects.filter(type=2, verified=False)
    @classmethod
    def get_penalty_photos(cls):
        types = Q(verified=False,type__gt=11)&Q(type__lt=15)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_videos(cls):
        types = Q(verified=False,type__gt=28)&Q(type__lt=32)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_audios(cls):
        types = Q(verified=False,type__gt=24)&Q(type__lt=27)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_survey(cls):
        types = Q(verified=False,type__gt=20)&Q(type__lt=23)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_docs(cls):
        types = Q(verified=False,type__gt=16)&Q(type__lt=19)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_sites(cls):
        return cls.objects.filter(type=6,verified=False)
    @classmethod
    def get_penalty_articles(cls):
        return cls.objects.filter(type=7,verified=False)
    @classmethod
    def get_penalty_goods(cls):
        types = Q(verified=False,type__gt=32)&Q(type__lt=36)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_planner(cls):
        types = Q(verified=False,type__gt=37)&Q(type__lt=43)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_forum(cls):
        types = Q(verified=False,type__gt=44)&Q(type__lt=47)
        return cls.objects.filter(types)
    @classmethod
    def get_penalty_wiki(cls):
        types = Q(verified=False,type__gt=48)&Q(type__lt=51)
        return cls.objects.filter(types)

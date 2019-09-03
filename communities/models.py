from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.db.models import Count
from pilkit.processors import ResizeToFill, ResizeToFit
from communities.helpers import upload_to_community_avatar_directory, upload_to_community_cover_directory
from communities.validators import community_name_characters_validator
#from posts.models import Post
from imagekit.models import ProcessedImageField
#from users.models import User
#from moderation.models import ModeratedObject, ModerationCategory



class Community(models.Model):
    #moderated_object = GenericRelation(ModeratedObject, related_query_name='communities',verbose_name="Модерация")
    #creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities', null=False,blank=False,verbose_name="Создатель")
    name = models.CharField(max_length=100, blank=False, null=False,
                            unique=True, validators=(community_name_characters_validator,),verbose_name="Имя")
    title = models.CharField(max_length=100, blank=False, null=False,verbose_name="Заголовок" )
    description = models.CharField(max_length=300, blank=False,
                                   null=True,verbose_name="Описание" )
    rules = models.TextField(max_length=100, blank=False,
                             null=True,verbose_name="Правила")
    avatar = ProcessedImageField(blank=False, null=True, format='JPEG',
                                 options={'quality': 90}, processors=[ResizeToFill(500, 500)],
                                 upload_to=upload_to_community_avatar_directory,verbose_name="Аватар")
    cover = ProcessedImageField(blank=False, null=True, format='JPEG',
                                options={'quality': 90},
                                upload_to=upload_to_community_cover_directory,
                                processors=[ResizeToFit(width=1024, upscale=False)],verbose_name="Фон")
    created = models.DateTimeField(editable=False,verbose_name="Создано")
    #starrers = models.ManyToManyField(User, related_name='favorite_communities',verbose_name="Подписчики")
    #banned_users = models.ManyToManyField(User, related_name='banned_of_communities',verbose_name="Черный список")
    COMMUNITY_TYPE_PRIVATE = 'T'
    COMMUNITY_TYPE_PUBLIC = 'P'
    COMMUNITY_TYPES = (
        (COMMUNITY_TYPE_PUBLIC, 'Публичное'),
        (COMMUNITY_TYPE_PRIVATE, 'Приватное'),
    )
    type = models.CharField(editable=False, blank=False, null=False, choices=COMMUNITY_TYPES, default='P', max_length=2)
    color = models.CharField(max_length=COLOR_ATTR_MAX_LENGTH, blank=False, null=False,
                             validators=[hex_color_validator],verbose_name="Цвет")
    user_adjective = models.CharField(max_length=100,
                                      blank=False, null=True,verbose_name="Какой-то пользователь")
    users_adjective = models.CharField(100,
                                       blank=False, null=True,verbose_name="Какие-то пользователи")
    invites_enabled = models.BooleanField(default=True,verbose_name="Разрешить приглашения")
    is_deleted = models.BooleanField(
        default=False,
        verbose_name="Удаленное"
    )

    class Meta:
        verbose_name_plural = 'сообщества'


class CommunityMembership(models.Model):
    """
    Объект, представляющий членство пользователя в сообществе
    """
    #user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities_memberships', null=False,blank=False,verbose_name="Члены сообщества")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='memberships', null=False,blank=False,verbose_name="Сообщество")
    is_administrator = models.BooleanField(default=False,verbose_name="Это администратор")
    is_moderator = models.BooleanField(default=False,verbose_name="Это модератор")
    created = models.DateTimeField(editable=False,verbose_name="Создано")


class CommunityLog(models.Model):
    """
    Журнал для действий пользователей модераторов сообщества, таких как запрет / снятие блокировки
    """
    #source_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=False,blank=False,verbose_name="Кто модерирует")
    #target_user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True,blank=False,verbose_name="Кого модерируют")
    #post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', null=True, blank=True,verbose_name="Пост")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='logs',null=False,blank=False,verbose_name="Сообщество")
    created = models.DateTimeField(editable=False,verbose_name="Создан")

    ACTION_TYPES = (
        ('B', 'Заблокировать'),
        ('U', 'Разблокировать'),
        ('AM', 'Добавить модератора'),
        ('RM', 'Удалить модератора'),
        ('AA', 'Добавить администратора'),
        ('RA', 'Удалить администратора'),
        ('OP', 'Открыть пост'),
        ('CP', 'Закрыть пост'),
        ('RP', 'Удалить пост'),
        ('RPC', 'Удалить комментарий к посту'),
        ('DPC', 'Отключить комментарии'),
        ('EPC', 'Включить комментарии'),
    )
    action_type = models.CharField(editable=False, blank=False, null=False, choices=ACTION_TYPES, max_length=5)


class CommunityInvite(models.Model):
    #creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_communities_invites', null=False,blank=False,verbose_name="Кто приглашает в сообщество")
    #invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='communities_invites', null=False,blank=False,verbose_name="Кого приглашают в сообщество")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='invites', null=False,blank=False,verbose_name="Сообщество")

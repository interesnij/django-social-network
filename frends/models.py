from django.db import models
from django.conf import settings


class Connect(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='connections', verbose_name="Инициатор перевода из подписчика в друзья")
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='targeted_connections', null=False, verbose_name="Кого переводит из подписчика в друзья")
    target_connection = models.OneToOneField('self', on_delete=models.CASCADE, null=True)
    visited = models.PositiveIntegerField(default=0, verbose_name="Количество визитов")

    @classmethod
    def create_connection(cls, user_id, target_user_id):
        target_connection = cls.objects.create(user_id=target_user_id, target_user_id=user_id)
        connection = cls.objects.create(user_id=user_id, target_user_id=target_user_id,target_connection=target_connection)
        target_connection.target_connection = connection
        target_connection.save()
        connection.save()
        return connection

    class Meta:
        unique_together = ('user', 'target_user')
        verbose_name = 'Друг'
        verbose_name_plural = 'Друзья'
        ordering = ["-visited"]

    @classmethod
    def connection_exists(cls, user_a_id, user_b_id):
        count = cls.objects.select_related('target_connection__user_id').filter(user_id=user_a_id,                                                                           target_connection__user_id=user_b_id).count()
        return count > 0

    @classmethod
    def connection_with_id_exists_for_user_with_id(cls, connection_id, user_id):
        count = cls.objects.filter(id=connection_id, user_id=user_id).count()
        if count > 0:
            return True
        return False

    def delete_perm(self, type):
        try:
            perm = self.connect_ie_settings
            if type == "can_see_community":
                perm.can_see_community = 0
                perm.save(update_fields=["can_see_community"])
        except ConnectPerm.DoesNotExist:
            pass


class ConnectPerm(models.Model):
    """ связь с таблицей друзей target_user. Появляется после ее инициирования, когда друг записи Connect
        добавит какое либо исключение или включение для какого-либо элемента.
        1. NO_VALUE - неактивное значение.
        2. YES_ITEM - может соверщать описанные действия
        3. NO_ITEM - не может соверщать описанные действия
    """
    NO_VALUE, YES_ITEM, NO_ITEM = 0, 1, 2
    ITEM = (
        (NO_VALUE, 'Не активно'),
        (YES_ITEM, 'Может иметь действия с элементом'),
        (NO_ITEM, 'Не может иметь действия с элементом'),
    )

    user = models.OneToOneField(Connect, null=True, blank=True, on_delete=models.CASCADE, related_name='connect_ie_settings', verbose_name="Друг")

    can_see_info = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит информацию профиля")
    can_see_community = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит сообщества")
    can_see_friend = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит друзей")
    can_send_message = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто пишет сообщения")
    can_add_in_chat = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет в беседы")
    can_see_doc = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит документы и списки")
    can_see_music = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит музыку и списки")

    can_see_post = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит записи и списки")
    can_see_post_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комменты к записям")

    can_see_photo = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит фото и списки")
    can_see_photo_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комменты к фото")

    can_see_good = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит товары и списки")
    can_see_good_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комменты к товарам")

    can_see_video = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит видео и списки")
    can_see_video_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комменты к видео")

    can_see_planner = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит рабочие пространства и доски")
    can_see_planner_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комменты к доскам")

    can_copy_post = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто копирует записи и списки")
    can_copy_photo = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто копирует фото и списки")
    can_copy_good = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто копирует товары и списки")
    can_copy_video = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто копирует видео и списки")
    can_copy_planner = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто копирует рабочие пространства и доски")
    can_copy_doc = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто копирует документы и списки")
    can_copy_music = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто копирует музыку и списки")

    can_create_post = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает записи и списки, работает с ними")
    can_create_post_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комменты к записям")

    can_create_photo = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает фото и списки, работает с ними")
    can_create_photo_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комменты к фото")

    can_create_good = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает товары и списки, работает с ними")
    can_create_good_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комменты к товарам")

    can_create_video = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает видео и списки, работает с ними")
    can_create_video_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комменты к видео")

    can_create_planner = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает рабочие пространства и доски, работает с ними")
    can_create_planner_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комменты к задачам")

    can_create_doc = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает документы и списки, работает с ними")
    can_create_music = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает музыку и списки, работает с ними")

    class Meta:
        verbose_name = 'Исключения/Включения target_user'
        verbose_name_plural = 'Исключения/Включения target_user'
        index_together = [('id', 'user'),]

    @classmethod
    def get_or_create_perm(cls, user_id, target_user_id, ):
        frend = Connect.objects.get(user_id=user_id, target_user_id=target_user_id)
        if cls.objects.filter(user_id=frend.pk).exists():
            return cls.objects.get(user_id=frend.pk)
        else:
            perm = cls.objects.create(user_id=frend.pk)
            return perm

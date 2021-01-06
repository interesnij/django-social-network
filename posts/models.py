import uuid
from django.db import models
from django.conf import settings
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from django.contrib.postgres.indexes import BrinIndex
from django.utils import timezone
from notify.model.post import *
from common.utils import try_except


class PostList(models.Model):
    MAIN, LIST, PRIVATE, DELETED, FIX = 'MA', 'LI', 'PR', 'DE', 'FI'
    TYPE = (
        (MAIN, 'Основной список'),
        (LIST, 'Пользовательский список'),
		(PRIVATE, 'Приватный список'),
		(DELETED, 'Архивный список'),
        (FIX, 'Закрепленный список'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_postlist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_postlist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=LIST, verbose_name="Тип листа")
    order = models.PositiveIntegerField(default=1)
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)

    def __str__(self):
        return self.name + " - " + self.creator.get_full_name()

    def is_post_in_list(self, post_id):
        return self.post_list.filter(pk=post_id).values("pk").exists()

    def is_not_empty(self):
        return self.post_list.filter(list=self).values("pk").exists()

    def get_posts(self):
        select_related = ('creator', 'community')
        only = ('creator__id', 'community__id', 'created')
        prefetch_related = ('post_album', 'item_photo', 'post_doclist', 'item_doc', 'attached_item', 'post_good_album', 'item_good', 'post_soundlist', 'item_music', 'item_video', 'post_video_album')
        posts = self.post_list.select_related(*select_related).prefetch_related(*prefetch_related).only(*only).filter(list=self, is_deleted=False, status="P").order_by("-created")
        return posts

    def list_30(self):
        queryset = self.post_list.only("pk")[:30].order_by('-created')
        return queryset
    def list_6(self):
        queryset = self.post_list.only("pk")[:6].order_by('-created')
        return queryset

    def count_posts(self):
        return self.post_list.filter(is_deleted=False).values("pk").count()
    def get_posts_ids(self):
        ids =  self.post_list.filter(is_deleted=False).values("pk")
        return [id['pk'] for id in ids]

    def is_full_list(self):
        if self.is_fix_list() and self.count_posts() == 10:
            return True
        else:
            return False

    def is_main_list(self):
        return self.type == self.MAIN
    def is_fix_list(self):
        return self.type == self.FIX
    def is_list_list(self):
        return self.type == self.LIST
    def is_deleted_list(self):
        return self.type == self.DELETED
    def is_private_list(self):
        return self.type == self.PRIVATE
    def is_user_list(self):
        if self.type == self.LIST or self.type == self.PRIVATE:
            return True
        else:
            return False

    class Meta:
        verbose_name = "список записей"
        verbose_name_plural = "списки записей"
        ordering = ['order']


class PostCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Тематика")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Тематика постов"
		verbose_name_plural = "Тематики постов"


class Post(models.Model):
    STATUS_DRAFT, STATUS_PROCESSING, STATUS_MESSAGE_PUBLISHED, STATUS_PUBLISHED = 'D', 'PG', 'MP', 'P'
    PHOTO_REPOST, PHOTO_ALBUM_REPOST, GOOD_REPOST, GOOD_LIST_REPOST, MUSIC_REPOST, MUSIC_LIST_REPOST, DOC_REPOST, \
    DOC_LIST_REPOST, VIDEO_REPOST, VIDEO_LIST_REPOST, USER_REPOST, COMMUNITY_REPOST = 'PR', 'PAR', 'GR', 'GLR', 'MR', 'MLR', 'DR', \
    'DLR', 'VR', 'VLR', 'UR', 'CR'
    STATUSES = (
        (STATUS_DRAFT,'Черновик'),(STATUS_PROCESSING,'Обработка'),(STATUS_PUBLISHED,'Опубликована'),(STATUS_MESSAGE_PUBLISHED,'Репост в сообщения'),
        (PHOTO_REPOST, 'Репост фотографии'), (PHOTO_ALBUM_REPOST, 'Репост фотоальбома'),
        (GOOD_REPOST, 'Репост товара'), (GOOD_LIST_REPOST, 'Репост списка товаров'),
        (MUSIC_REPOST, 'Репост аудиозаписи'), (MUSIC_LIST_REPOST, 'Репост плейлиста аудиозаписей'),
        (DOC_REPOST, 'Репост документа'), (DOC_LIST_REPOST, 'Репост списка документов'),
        (VIDEO_REPOST, 'Репост видеозаписи'), (VIDEO_LIST_REPOST, 'Репост списка видеозаписей'),
        (USER_REPOST, 'Репост пользователя'), (COMMUNITY_REPOST, 'Репост сообщества'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")

    community = models.ForeignKey('communities.Community', related_name='post_community', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="thread")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='post_creator', on_delete=models.SET_NULL, verbose_name="Создатель")
    category = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Тематика")
    list = models.ManyToManyField(PostList, related_name='post_list')

    created = models.DateTimeField(default=timezone.now, verbose_name="Создан")
    status = models.CharField(choices=STATUSES, default=STATUS_PROCESSING, max_length=5, verbose_name="Статус статьи")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Текст")

    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    is_signature = models.BooleanField(default=True, verbose_name="Подпись автора")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.creator.get_full_name()

    @classmethod
    def create_post(cls, creator, text, category, lists, attach, community, parent, comments_enabled, is_signature, votes_on, status):
        if not lists:
            raise ValidationError("Не выбран список для новой записи")
        _attach = str(attach)
        post = Post.objects.create(creator=creator,
                                    text=text,
                                    category=category,
                                    community=community,
                                    parent=parent,
                                    comments_enabled=comments_enabled,
                                    is_signature=is_signature,
                                    votes_on=votes_on,
                                    status=status,
                                    attach=_attach.replace("[", "").replace("'", "").replace("]", "").replace(" ", ""),)
        for list_id in lists:
            post_list = PostList.objects.get(pk=list_id)
            post_list.post_list.add(post)
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "create_item",
			'creator_id': post.creator.pk,
			'post_id': str(post.uuid),
			'name': "u_post_create",
            }
        async_to_sync(channel_layer.group_send)('notification', payload)
        return post

    @classmethod
    def create_parent_post(cls, creator, community, status):
        post = cls.objects.create(creator=creator, community=community, status=status, )
        return post

    def is_photo_repost(self):
        return try_except(self.status == Post.PHOTO_REPOST)
    def get_photo_repost(self):
        photo = self.parent.item_photo.filter(is_deleted=False)[0]
        return photo
    def is_photo_album_repost(self):
        return try_except(self.status == Post.PHOTO_ALBUM_REPOST)
    def get_photo_album_repost(self):
        photo_album = self.parent.post_album.filter(is_deleted=False)[0]
        return photo_album

    def is_music_repost(self):
        return try_except(self.status == Post.MUSIC_REPOST)
    def is_music_list_repost(self):
        return try_except(self.status == Post.MUSIC_LIST_REPOST)
    def get_playlist_repost(self):
        playlist = self.parent.post_soundlist.filter(is_deleted=False)[0]
        return playlist
    def get_music_repost(self):
        music = self.parent.item_music.filter(is_deleted=False)[0]
        return music

    def is_good_repost(self):
        return try_except(self.status == Post.GOOD_REPOST)
    def is_good_list_repost(self):
        return try_except(self.status == Post.GOOD_LIST_REPOST)
    def get_good_repost(self):
        good = self.parent.item_good.filter(is_deleted=False)[0]
        return good
    def get_good_list_repost(self):
        good_list = self.parent.post_good_album.filter(is_deleted=False)[0]
        return good_list

    def is_doc_repost(self):
        return try_except(self.status == Post.DOC_REPOST)
    def is_doc_list_repost(self):
        return try_except(self.status == Post.DOC_LIST_REPOST)
    def get_doc_list_repost(self):
        list = self.parent.post_doclist.filter(is_deleted=False)[0]
        return list
    def get_doc_repost(self):
        doc = self.parent.item_doc.filter(is_deleted=False)[0]
        return doc

    def is_video_repost(self):
        return try_except(self.status == Post.VIDEO_REPOST)
    def is_video_list_repost(self):
        return try_except(self.status == Post.VIDEO_LIST_REPOST)
    def get_video_list_repost(self):
        video_list = self.parent.post_video_album.filter(is_deleted=False)[0]
        return video_list

    def is_user_repost(self):
        return try_except(self.status == Post.USER_REPOST)
    def is_community_repost(self):
        return try_except(self.status == Post.COMMUNITY_REPOST)

    def get_c_post_parent_items_desctop(self):
        # метод выясняет, есть ли у поста-родителя в сообществе прикрепленные большие элементы, а также их репосты.
        # Поскольку в пост влезает только один большой элемент, то это разгружает шаблонные расчеты, сразу выдавая
        # шаблон вложения или репоста большого элемента. Если же таких нет, то остаток работы (проверка на репосты и вложения маленьких элементов)
        # придется совершать в шаблоне, ведь варианты работы с небольшими элементами очень обширны.
		# FOR DESCTOP PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "desctop/generic/repost/c_photo_repost.html"
        elif parent.is_photo_album_repost():
            return "desctop/generic/repost/c_photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "desctop/generic/parent_attach/c_photo_list_attach.html"
        elif parent.is_good_repost():
            return "desctop/generic/repost/c_good_repost.html"
        elif parent.is_good_list_repost():
            return "desctop/generic/repost/c_good_list_repost.html"
        elif parent.is_good_list_attached():
            return "desctop/generic/parent_attach/c_good_list_attach.html"
        elif parent.is_music_repost():
            return "desctop/generic/repost/c_music_repost.html"
        elif parent.is_music_list_repost():
            return "desctop/generic/repost/c_music_list_repost.html"
        elif parent.is_playlist_attached():
            return "desctop/generic/parent_attach/c_playlist_attach.html"
        elif parent.is_video_repost():
            return "desctop/generic/repost/c_video_repost.html"
        elif parent.is_video_list_repost():
            return "desctop/generic/repost/c_video_list_repost.html"
        elif parent.is_video_list_attached():
            return "desctop/generic/parent_attach/c_video_list_attach.html"
        elif parent.is_doc_repost():
            return "desctop/generic/repost/c_doc_repost.html"
        elif parent.is_doc_list_repost():
            return "desctop/generic/repost/c_doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "desctop/generic/parent_attach/c_doc_list_attach.html"
        elif parent.is_user_repost():
            return "desctop/generic/repost/user_repost.html"
        elif parent.is_community_repost():
            return "desctop/generic/repost/community_repost.html"
        else:
            return "desctop/generic/attach/parent_community.html"

    def get_u_post_parent_items_desctop(self):
        # метод выясняет, есть ли у поста-родителя пользователя прикрепленные большие элементы, а также их репосты.
        # Поскольку в пост влезает только один большой элемент, то это разгружает шаблонные расчеты, сразу выдавая
        # шаблон вложения или репоста большого элемента. Если же таких нет, то остаток работы (проверка на репосты и вложения маленьких элементов)
        # придется совершать в шаблоне, ведь варианты работы с небольшими элементами очень обширны.
		# FOR DESCTOP PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "desctop/generic/repost/u_photo_repost.html"
        elif parent.is_photo_album_repost():
            return "desctop/generic/repost/u_photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "desctop/generic/parent_attach/u_photo_list_attach.html"
        elif parent.is_good_repost():
            return "desctop/generic/repost/u_good_repost.html"
        elif parent.is_good_list_repost():
            return "desctop/generic/repost/u_good_list_repost.html"
        elif parent.is_good_list_attached():
            return "desctop/generic/parent_attach/u_good_list_attach.html"
        elif parent.is_music_repost():
            return "desctop/generic/repost/u_music_repost.html"
        elif parent.is_music_list_repost():
            return "desctop/generic/repost/u_music_list_repost.html"
        elif parent.is_playlist_attached():
            return "desctop/generic/parent_attach/u_playlist_attach.html"
        elif parent.is_video_repost():
            return "desctop/generic/repost/u_video_repost.html"
        elif parent.is_video_list_repost():
            return "desctop/generic/repost/u_video_list_repost.html"
        elif parent.is_video_list_attached():
            return "desctop/generic/parent_attach/u_video_list_attach.html"
        elif parent.is_doc_repost():
            return "desctop/generic/repost/u_doc_repost.html"
        elif parent.is_doc_list_repost():
            return "desctop/generic/repost/u_doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "desctop/generic/parent_attach/u_doc_list_attach.html"
        elif parent.is_user_repost():
            return "desctop/generic/repost/u_user_repost.html"
        elif parent.is_community_repost():
            return "desctop/generic/repost/u_community_repost.html"
        else:
            return "desctop/generic/attach/parent_user.html"

    def get_u_news_parent_desctop(self):
		# FOR DESCTOP PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "desctop/posts/u_posts/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "desctop/posts/u_posts/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "desctop/generic/parent_attach/u_photo_list_attach.html"
        elif parent.is_good_repost():
            return "desctop/posts/u_posts/good_repost.html"
        elif parent.is_good_list_repost():
            return "desctop/posts/u_posts/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "desctop/generic/parent_attach/u_good_list_attach.html"
        elif parent.is_music_repost():
            return "desctop/posts/u_posts/music_repost.html"
        elif parent.is_music_list_repost():
            return "desctop/posts/u_posts/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "desctop/generic/parent_attach/u_playlist_attach.html"
        elif parent.is_video_repost():
            return "desctop/posts/u_posts/video_repost.html"
        elif parent.is_video_list_repost():
            return "desctop/posts/u_posts/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "desctop/generic/parent_attach/u_video_list_attach.html"
        elif parent.is_doc_repost():
            return "desctop/posts/u_posts/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "desctop/posts/u_posts/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "desctop/generic/parent_attach/u_doc_list_attach.html"
        elif parent.is_user_repost():
            return "desctop/posts/u_posts/user_repost.html"
        elif parent.is_community_repost():
            return "desctop/posts/u_posts/community_repost.html"
        else:
            return "desctop/posts/u_posts/parent_user.html"

    def get_c_news_parent_desctop(self):
		# FOR DESCTOP PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "desctop/posts/c_posts/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "desctop/posts/c_posts/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "desctop/generic/parent_attach/c_photo_list_attach.html"
        elif parent.is_good_repost():
            return "desctop/posts/c_posts/good_repost.html"
        elif parent.is_good_list_repost():
            return "desctop/posts/c_posts/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "desctop/generic/parent_attach/c_good_list_attach.html"
        elif parent.is_music_repost():
            return "desctop/posts/c_posts/music_repost.html"
        elif parent.is_music_list_repost():
            return "desctop/posts/c_posts/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "desctop/generic/parent_attach/c_playlist_attach.html"
        elif parent.is_video_repost():
            return "desctop/posts/c_posts/video_repost.html"
        elif parent.is_video_list_repost():
            return "desctop/posts/c_posts/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "desctop/generic/parent_attach/c_video_list_attach.html"
        elif parent.is_doc_repost():
            return "desctop/posts/c_posts/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "desctop/posts/c_posts/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "desctop/generic/parent_attach/c_doc_list_attach.html"
        elif parent.is_user_repost():
            return "desctop/posts/c_posts/user_repost.html"
        elif parent.is_community_repost():
            return "desctop/posts/c_posts/community_repost.html"
        else:
            return "desctop/posts/c_posts/parent_community.html"

    def get_c_post_parent_items_mobile(self):
        # метод выясняет, есть ли у поста-родителя в сообществе прикрепленные большие элементы, а также их репосты.
        # Поскольку в пост влезает только один большой элемент, то это разгружает шаблонные расчеты, сразу выдавая
        # шаблон вложения или репоста большого элемента. Если же таких нет, то остаток работы (проверка на репосты и вложения маленьких элементов)
        # придется совершать в шаблоне, ведь варианты работы с небольшими элементами очень обширны.
		# FOR MOBILE PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "mobile/generic/repost/c_photo_repost.html"
        elif parent.is_photo_album_repost():
            return "mobile/generic/repost/c_photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "mobile/generic/parent_attach/c_photo_list_attach.html"
        elif parent.is_good_repost():
            return "mobile/generic/repost/c_good_repost.html"
        elif parent.is_good_list_repost():
            return "mobile/generic/repost/c_good_list_repost.html"
        elif parent.is_good_list_attached():
            return "mobile/generic/parent_attach/c_good_list_attach.html"
        elif parent.is_music_repost():
            return "mobile/generic/repost/c_music_repost.html"
        elif parent.is_music_list_repost():
            return "mobile/generic/repost/c_music_list_repost.html"
        elif parent.is_playlist_attached():
            return "mobile/generic/parent_attach/c_playlist_attach.html"
        elif parent.is_video_repost():
            return "mobile/generic/repost/c_video_repost.html"
        elif parent.is_video_list_repost():
            return "mobile/generic/repost/c_video_list_repost.html"
        elif parent.is_video_list_attached():
            return "mobile/generic/parent_attach/c_video_list_attach.html"
        elif parent.is_doc_repost():
            return "mobile/generic/repost/c_doc_repost.html"
        elif parent.is_doc_list_repost():
            return "mobile/generic/repost/c_doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "mobile/generic/parent_attach/c_doc_list_attach.html"
        elif parent.is_user_repost():
            return "mobile/generic/repost/c_user_repost.html"
        elif parent.is_community_repost():
            return "mobile/generic/repost/c_community_repost.html"
        else:
            return "mobile/generic/attach/parent_community.html"

    def get_u_post_parent_items_mobile(self):
        # метод выясняет, есть ли у поста-родителя пользователя прикрепленные большие элементы, а также их репосты.
        # Поскольку в пост влезает только один большой элемент, то это разгружает шаблонные расчеты, сразу выдавая
        # шаблон вложения или репоста большого элемента. Если же таких нет, то остаток работы (проверка на репосты и вложения маленьких элементов)
        # придется совершать в шаблоне, ведь варианты работы с небольшими элементами очень обширны.
		# FOR MOBILE PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "mobile/generic/repost/u_photo_repost.html"
        elif parent.is_photo_album_repost():
            return "mobile/generic/repost/u_photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "mobile/generic/parent_attach/u_photo_list_attach.html"
        elif parent.is_good_repost():
            return "mobile/generic/repost/u_ood_repost.html"
        elif parent.is_good_list_repost():
            return "mobile/generic/repost/u_good_list_repost.html"
        elif parent.is_good_list_attached():
            return "mobile/generic/parent_attach/u_good_list_attach.html"
        elif parent.is_music_repost():
            return "mobile/generic/repost/u_music_repost.html"
        elif parent.is_music_list_repost():
            return "mobile/generic/repost/u_music_list_repost.html"
        elif parent.is_playlist_attached():
            return "mobile/generic/parent_attach/u_playlist_attach.html"
        elif parent.is_video_repost():
            return "mobile/generic/repost/u_video_repost.html"
        elif parent.is_video_list_repost():
            return "mobile/generic/repost/u_video_list_repost.html"
        elif parent.is_video_list_attached():
            return "mobile/generic/parent_attach/u_video_list_attach.html"
        elif parent.is_doc_repost():
            return "mobile/generic/repost/u_doc_repost.html"
        elif parent.is_doc_list_repost():
            return "mobile/generic/repost/u_doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "mobile/generic/parent_attach/u_doc_list_attach.html"
        elif parent.is_user_repost():
            return "mobile/generic/repost/u_user_repost.html"
        elif parent.is_community_repost():
            return "mobile/generic/repost/u_community_repost.html"
        else:
            return "mobile/generic/attach/parent_user.html"

    def get_u_news_parent_mobile(self):
		# FOR MOBILE PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "mobile/main/u_posts/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "mobile/main/u_posts/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "mobile/generic/parent_attach/u_photo_list_attach.html"
        elif parent.is_good_repost():
            return "mobile/main/u_posts/good_repost.html"
        elif parent.is_good_list_repost():
            return "mobile/main/u_posts/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "mobile/generic/parent_attach/u_good_list_attach.html"
        elif parent.is_music_repost():
            return "mobile/main/u_posts/music_repost.html"
        elif parent.is_music_list_repost():
            return "mobile/main/u_posts/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "mobile/generic/parent_attach/u_playlist_attach.html"
        elif parent.is_video_repost():
            return "mobile/main/u_posts/video_repost.html"
        elif parent.is_video_list_repost():
            return "mobile/main/u_posts/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "mobile/generic/parent_attach/u_video_list_attach.html"
        elif parent.is_doc_repost():
            return "mobile/main/u_posts/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "mobile/main/u_posts/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "mobile/generic/parent_attach/u_doc_list_attach.html"
        elif parent.is_user_repost():
            return "mobile/main/u_posts/user_repost.html"
        elif parent.is_community_repost():
            return "mobile/main/u_posts/community_repost.html"
        else:
            return "mobile/main/u_posts/parent_user.html"

    def get_c_news_parent_mobile(self):
		# FOR MOBILE PLATFORM
        parent = self.parent
        if parent.is_photo_repost():
            return "mobile/main/c_posts/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "mobile/main/c_posts/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "mobile/generic/parent_attach/c_photo_list_attach.html"
        elif parent.is_good_repost():
            return "mobile/main/c_posts/good_repost.html"
        elif parent.is_good_list_repost():
            return "mobile/main/c_posts/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "mobile/generic/parent_attach/c_good_list_attach.html"
        elif parent.is_music_repost():
            return "mobile/main/c_posts/music_repost.html"
        elif parent.is_music_list_repost():
            return "mobile/main/c_posts/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "mobile/generic/parent_attach/c_playlist_attach.html"
        elif parent.is_video_repost():
            return "mobile/main/c_posts/video_repost.html"
        elif parent.is_video_list_repost():
            return "mobile/main/c_posts/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "mobile/generic/parent_attach/c_video_list_attach.html"
        elif parent.is_doc_repost():
            return "mobile/main/c_posts/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "mobile/main/c_posts/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "mobile/generic/parent_attach/c_doc_list_attach.html"
        elif parent.is_user_repost():
            return "mobile/main/c_posts/user_repost.html"
        elif parent.is_community_repost():
            return "mobile/main/c_posts/community_repost.html"
        else:
            return "mobile/main/c_posts/parent_community.html"

    def get_u_attach(self, user):
        block = ''
        for item in self.attach.split(","):
            if item[:3] == "pho":
                from gallery.models import Photo
                photo = Photo.objects.get(pk=item[3:], is_public=True)
                block = ''.join([block, '<div class="photo"><div class="progressive replace image_fit u_post_photo pointer" data-href="', photo.file.url, '" photo-pk="', str(photo.pk), '"><img class="preview image_fit" width="20" height="15" loading="lazy" src="', photo.preview.url,'" alt="img"></div></div>'])
            elif item[:3] == "vid":
                from video.models import Video
                video = Video.objects.get(pk=item[3:], is_public=True)
                block = ''.join([block, '<div class="video"><img class="image_fit" src="', video.image.url, '" alt="img"><div class="video_icon_play_v2 u_post_video" data-pk="', video.creator.pk, '" video-pk="', video.pk, '" data-uuid="', object.uuid, '" video-counter="0"></div></div>'])
            elif item[:3] == "mus":
                from music.models import SoundcloudParsing
                music = SoundcloudParsing.objects.get(pk=item[3:])
                if music.artwork_url:
                    figure = '<figure><a class="music_list_post music_thumb pointer"><img style="width:30px;heigth:auto" src="', music.artwork_url, '" alt="img" /></a></figure>'
                else:
                    figure = '<figure><a class="music_list_post music_thumb pointer"><svg fill="currentColor" style="width:30px;heigth:30px" class="svg_default" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-2 5h-3v5.5c0 1.38-1.12 2.5-2.5 2.5S10 13.88 10 12.5s1.12-2.5 2.5-2.5c.57 0 1.08.19 1.5.51V5h4v2zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6z"/></svg></a></figure>'
                lists = ''
                for list in user.get_all_audio_playlists():
                    if list.is_track_in_list(music.pk):
                        lists = ''.join([lists, '<span data-uuid="', str(list.uuid), '"><span class="dropdown-item u_remove_track_in_list"><svg fill="currentColor" style="width:15px;height:15px;" class="svg_default" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>', list.name, '</span>'])
                    else:
                        lists = ''.join([lists, '<span class="dropdown-item u_add_track_in_list" style="padding-left: 30px;">', list.name, '</span>'])
                block = ''.join([block, '<div class="music" data-path="', music.uri, '" data-duration="', music.duration, '" style="flex-basis: 100%;position: relative;"><div class="media" music-counter="', forloop.counter0, '">', figure, '<div class="media-body" style="display: flex;"><h6 class="music_list_post music_title"><a>', music.title, '</a></h6><span class="span_btn" style="margin-left:auto;display:flex" data-pk="', music.pk, '" user-pk="', object.creator.pk, '"><span class="dropdown" style="position: inherit;"><span class="btn_default pointer drop"><svg fill="currentColor" style="width:25px;height:25px;" class="svg_default" viewBox="0 0 24 24"><path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/><path d="M0 0h24v24H0z" fill="none"/></svg></span><div class="dropdown-menu dropdown-menu-right" style="top: 25px;">', lists, '<span class="dropdown-item u_create_music_list_track_add" style="padding-left: 30px;">В новый плейлист</span></div></span><span class="u_ucm_music_repost btn_default pointer"><svg class="svg_default" style="width:20px;height:20px;" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z"/></svg></span></span></div></div></div>'])
            elif item[:3] == "goo":
                from goods.models import Good
                good = Good.objects.get(pk=item[3:])
                if good.image:
                    figure = '<figure class="background-img shadow-dark"><img class="image_fit opacity-100" src="', good.image.url, '" alt="img"></figure>'
                else:
                    figure = '<figure class="background-img shadow-dark"><svg class="image_fit svg_default opacity-100" fill="currentColor" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none" /><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg>'
                block = ''.join([block, '<div class="card has-background-img u_good_detail mb-3 pointer" good-pk="', good.pk, '" data-uuid="', good.get_album_uuid, '" style="flex-basis: 100%;">', figure, '<div class="card-header"><div class="media"><div class="media-body"><h4 class="text-white mb-0">', good.title, '</h4></div></div></div><div class="card-body spantshirt"></div><div class="card-footer"><p class="small mb-1 text-success">', good.price, ' ₽</p></div></div>'])
            elif item[:3] == "art":
                from article.models import Article
                article = Article.objects.get(pk=item[3:])
                if article.g_image:
                    figure = '<div class="align-items-center"><img class="image_fit" src="', article.g_image.url, '" alt="img"></div>'
                else:
                    figure = '<div class="align-items-center"><img class="image_fit" src="/static/images/no-image.jpg" alt="img" /></div>'
                block = ''.join([block, '<div class="article" data-uuid="', article.uuid, '"><span class="badge badge-info mb-2" style="position: absolute;bottom:-8px;"><svg style="padding-bottom: 1px" height="13" fill="#FFFFFF" viewBox="0 0 24 24" width="13"><path d="M0 0h24v24H0z" fill="none"/><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/></svg>', article.title, '</span><div class="text-center u_article_detail pointer">', figure, '</div></div>'])
            #elif item[:3] == "doc":
        return ''.join(["<div class='attach_container'>", block, "</div>"])


    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def count_comments(self):
        parent_comments = PostComment.objects.filter(post_id=self.pk, is_deleted=False)
        parents_count = parent_comments.count()
        i = 0
        for comment in parent_comments:
            i = i + comment.count_replies()
        i = i + parents_count
        return i

    def __str__(self):
        return self.creator.get_full_name()

    def get_comments(self):
        comments_query = Q(post_id=self.pk)
        comments_query.add(Q(parent_comment__isnull=True), Q.AND)
        return PostComment.objects.filter(comments_query)

    def is_fixed_in_community(self):
        try:
            list = PostList.objects.get(community_id=self.community.pk, type=PostList.FIX)
            if list.is_post_in_list(self.pk):
                return True
        except:
            pass
    def is_fixed_in_user(self):
        try:
            list = PostList.objects.get(creator_id=self.creator.pk, community__isnull=True, type=PostList.FIX)
            if list.is_post_in_list(self.pk):
                return True
        except:
            pass

    def is_can_fixed_in_community(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_community. Потому осталось проверить, не полон ли список"""
        try:
            list = PostList.objects.get(community_id=self.community.pk, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, community_id=self.community.pk, type=PostList.FIX, name="Закрепленный список")
        if list.is_full_list():
            return ValidationError("Запись нельзя прикрепить.")
        else:
            return True
    def is_can_fixed_in_user(self):
        """ мы уже проверили, есть ли пост в списке закрепов is_fixed_in_user. Потому осталось проверить, не полон ли список"""
        try:
            list = PostList.objects.get(creator_id=self.creator.pk, community__isnull=True, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, type=PostList.FIX, name="Закрепленный список")
        if list.is_full_list():
            return ValidationError("Запись нельзя прикрепить.")
        else:
            return True

    def fixed_user_post(self, user_id):
        try:
            list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=user_id, type=PostList.FIX, name="Закрепленный список")
        if not list.is_full_list():
            self.list.add(list)
            return True
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_user_post(self, user_id):
        try:
            list = PostList.objects.get(creator_id=user_id, community__isnull=True, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=user_id, type=PostList.FIX, name="Закрепленный список")
        if list.is_post_in_list(self.pk):
            self.list.remove(list)
            return True
        else:
            return ValidationError("Запись и так не в списке.")

    def fixed_community_post(self, community_id):
        try:
            list = PostList.objects.get(community_id=community_id, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, community_id=community_id, type=PostList.FIX, name="Закрепленный список")
        if not list.is_full_list():
            self.list.add(list)
            return True
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_community_post(self, community_id):
        try:
            list = PostList.objects.get(community_id=community_id, type=PostList.FIX)
        except:
            list = PostList.objects.create(creator_id=self.creator.pk, community_id=community_id, type=PostList.FIX, name="Закрепленный список")
        if list.is_post_in_list(self.pk):
            self.list.remove(list)
            return True
        else:
            return ValidationError("Запись и так не в списке.")

    def likes(self):
        from common.model.votes import PostVotes
        likes = PostVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def dislikes(self):
        from common.model.votes import PostVotes
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def likes_count(self):
        from common.model.votes import PostVotes
        likes = PostVotes.objects.filter(parent=self, vote__gt=0).values('pk').count()
        if likes > 0:
            return likes
        else:
            return ''

    def dislikes_count(self):
        from common.model.votes import PostVotes
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0).values('pk').count()
        if dislikes > 0:
            return dislikes
        else:
            return ''

    def window_likes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent=self, vote__gt=0)[0:6]

    def get_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents

    def get_window_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents[0:6]

    def count_reposts(self):
        parents = self.get_reposts()
        count_reposts = parents.values('pk').count()
        return count_reposts

    def get_visiter_sity(self):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        sities = UserLocation.objects.filter(user_id__in=ids).distinct('city_ru')
        return sities

    def get_sity_count(self, sity):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        count = UserLocation.objects.filter(user_id__in=ids, city_ru=sity).values('pk').count()
        return count

    def post_visits_count(self):
        from stst.models import PostNumbers
        return PostNumbers.objects.filter(post=self.pk).values('pk').count()
    def post_ad_visits_count(self):
        from stst.models import PostAdNumbers
        return PostAdNumbers.objects.filter(post=self.pk).values('pk').count()
    def all_visits_count(self):
        return self.post_visits_count() + self.post_ad_visits_count()

    def get_list_pk(self):
        return self.list.all()[0].pk

    def get_lists(self):
        return self.list.all()


class PostComment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    modified = models.DateTimeField(auto_now_add=True, auto_now=False, db_index=False)
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    is_edited = models.BooleanField(default=False, null=False, blank=False,verbose_name="Изменено")
    is_deleted = models.BooleanField(default=False,verbose_name="Удалено")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    id = models.BigAutoField(primary_key=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "комментарий к записи"
        verbose_name_plural = "комментарии к записи"

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        get_comments = PostComment.objects.filter(parent_comment=self).all()
        return get_comments

    def count_replies(self):
        return self.replies.filter(is_deleted=False).values("pk").count()

    def likes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__lt=0)

    def likes_count(self):
        from common.model.votes import PostCommentVotes
        qs = PostCommentVotes.objects.filter(item=self, vote__gt=0).values("pk").count()
        if qs > 0:
            return qs
        else:
            return ''

    def dislikes_count(self):
        from common.model.votes import PostCommentVotes
        qs = PostCommentVotes.objects.filter(item=self, vote__lt=0).values("pk").count()
        if qs > 0:
            return qs
        else:
            return ''

    def window_likes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__gt=0)[0:6]

    def window_dislikes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__lt=0)[0:6]

    def __str__(self):
        return self.commenter.get_full_name()

    @classmethod
    def create_comment(cls, commenter, post, parent_comment, text):
        comment = PostComment.objects.create(commenter=commenter, parent_comment=parent_comment, post=post, text=text, created=timezone.now())
        channel_layer = get_channel_layer()
        payload = {
            "type": "receive",
            "key": "comment_item",
            "actor_name": comment.commenter.get_full_name()
        }
        async_to_sync(channel_layer.group_send)('notifications', payload)
        return comment

    def count_replies_ru(self):
        count = self.replies.filter(is_deleted=False).values("pk").count()
        a, b= count % 10, count % 100
        if (a == 1) and (b != 11):
            return ''.join([str(count), " ответ"])
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return ''.join([str(count), " ответа"])
        else:
            return ''.join([str(count), " ответов"])

    def get_attach_photos(self):
        return self.comment_photo.all()
    def get_attach_videos(self):
        return self.comment_video.all()
    def get_attach_goods(self):
        return self.comment_good.all()
    def get_attach_articles(self):
        return self.attached_comment.all()
    def get_attach_tracks(self):
        return self.comment_music.all()
    def get_attach_docs(self):
        return self.comment_doc.all()

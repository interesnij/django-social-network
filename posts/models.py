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
from common.model.votes import PostVotes, PostCommentVotes
from common.utils import try_except


class PostList(models.Model):
    MAIN, LIST, PRIVATE, DELETED = 'MA', 'LI', 'PR', 'DE'
    TYPE = (
        (MAIN, 'Основной список'),
        (LIST, 'Пользовательский список'),
		(PRIVATE, 'Приватный список'),
		(DELETED, 'Удаленный список'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_postlist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_postlist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=5, choices=TYPE, default=LIST, verbose_name="Тип листа")
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " - " + self.creator.get_full_name()

    def is_post_in_list(self, post_id):
        return self.post_list.filter(pk=post_id).values("pk").exists()

    def is_not_empty(self):
        return self.post_list.filter(list=self).values("pk").exists()

    def get_posts(self):
        queryset = self.post_list.only("pk")
        return queryset

    def list_30(self):
        queryset = self.post_list.only("pk")[:30]
        return queryset
    def list_6(self):
        queryset = self.post_list.only("pk")[:6]
        return queryset

    def count_posts(self):
        return self.post_list.all().values("pk").count()

    def is_main_list(self):
        return self.type == self.MAIN
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
    PHOTO_REPOST, PHOTO_ALBUM_REPOST, GOOD_REPOST, GOOD_LIST_REPOST, MUSIC_REPOST, MUSIC_LIST_REPOST, DOC_REPOST, DOC_LIST_REPOST, VIDEO_REPOST, VIDEO_LIST_REPOST, USER_REPOST, COMMUNITY_REPOST = 'PR', 'PAR', 'GR', 'GLR', 'MR', 'MLR', 'DR', 'DLR', 'VR', 'VLR', 'UR', 'CR'
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
    is_fixed = models.BooleanField(default=False, verbose_name="Закреплено")
    is_signature = models.BooleanField(default=True, verbose_name="Подпись автора")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    id = models.BigAutoField(primary_key=True)
    is_deleted = models.BooleanField(verbose_name="Удален", default=False)

    @classmethod
    def create_post(cls, creator, text, category, lists, community, parent, comments_enabled, is_signature, votes_on, status):
        if not lists:
            raise ValidationError("Не выбран список для новой записи")
        post = Post.objects.create(creator=creator,
                                    text=text,
                                    category=category,
                                    community=community,
                                    parent=parent,
                                    comments_enabled=comments_enabled,
                                    is_signature=is_signature,
                                    votes_on=votes_on,
                                    status=status, )
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

    class Meta:
        ordering = ["-created"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.creator.get_full_name()

    def get_parent_attach_photos(self):
        return self.parent.item_photo.all()
    def get_parent_attach_photo_list(self):
        return self.parent.post_album.all()
    def get_parent_attach_videos(self):
        return self.parent.item_video.all()
    def get_parent_attach_video_list(self):
        return self.parent.post_video_album.all()
    def get_parent_attach_goods(self):
        return self.parent.item_good.all()
    def get_parent_attach_good_list(self):
        return self.parent.post_good_album.all()
    def get_parent_attach_articles(self):
        return self.parent.attached_item.all()
    def get_parent_attach_tracks(self):
        return self.parent.item_music.all()
    def get_parent_attach_music_list(self):
        return self.parent.post_soundlist.all()
    def get_parent_attach_docs(self):
        return self.parent.item_doc.all()
    def get_parent_attach_doc_list(self):
        return self.parent.post_doclist.all()

    def get_attach_photos(self):
        return self.item_photo.filter(is_deleted=False)
    def get_attach_photo_list(self):
        return self.post_album.filter(is_deleted=False)
    def get_attach_videos(self):
        return self.item_video.filter(is_deleted=False)
    def get_attach_video_list(self):
        return self.post_video_album.filter(is_deleted=False)
    def get_attach_goods(self):
        return self.item_good.filter(is_deleted=False)
    def get_attach_good_list(self):
        return self.post_good_album.filter(is_deleted=False)
    def get_attach_articles(self):
        return self.attached_item.filter(is_deleted=False)
    def get_attach_tracks(self):
        return self.item_music.filter(is_deleted=False)
    def get_attach_music_list(self):
        return self.post_soundlist.filter(is_deleted=False)
    def get_attach_docs(self):
        return self.item_doc.filter(is_deleted=False)
    def get_attach_doc_list(self):
        return self.post_doclist.filter(is_deleted=False)

    def is_photo_list_attached(self):
        return self.post_album.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_playlist_attached(self):
        return self.post_soundlist.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_video_list_attached(self):
        return self.post_video_album.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_good_list_attached(self):
        return self.post_good_album.filter(post__pk=self.pk, is_deleted=False).exists()
    def is_doc_list_attached(self):
        return self.post_doclist.filter(post__pk=self.pk, is_deleted=False).exists()

    def get_u_attach_items_desctop(self):
        if self.is_photo_list_attached():
            return "desctop/generic/attach/u_photo_list_attach.html"
        elif self.is_playlist_attached():
            return "desctop/generic/attach/u_playlist_attach.html"
        elif self.is_video_list_attached():
            return "desctop/generic/attach/u_video_list_attach.html"
        elif self.is_good_list_attached():
            return "desctop/generic/attach/u_good_list_attach.html"
        elif self.is_doc_list_attached():
            return "desctop/generic/attach/u_doc_list_attach.html"
        else:
            return "desctop/generic/attach/u_post_attach.html"

    def get_c_attach_items_desctop(self):
        if self.is_photo_list_attached():
            return "desctop/generic/attach/c_photo_list_attach.html"
        elif self.is_playlist_attached():
            return "desctop/generic/attach/c_playlist_attach.html"
        elif self.is_video_list_attached():
            return "desctop/generic/attach/c_video_list_attach.html"
        elif self.is_good_list_attached():
            return "desctop/generic/attach/c_good_list_attach.html"
        elif self.is_doc_list_attached():
            return "desctop/generic/attach/c_doc_list_attach.html"
        else:
            return "desctop/generic/attach/c_post_attach.html"

    def get_u_attach_items_mobile(self):
	    if self.is_photo_list_attached():
		    return "mobile/generic/attach/u_photo_list_attach.html"
	    elif self.is_playlist_attached():
		    return "mobile/generic/attach/u_playlist_attach.html"
	    elif self.is_video_list_attached():
		    return "mobile/generic/attach/u_video_list_attach.html"
	    elif self.is_good_list_attached():
		    return "mobile/generic/attach/u_good_list_attach.html"
	    elif self.is_doc_list_attached():
		    return "mobile/generic/attach/u_doc_list_attach.html"
	    else:
	        return "mobile/generic/attach/u_post_attach.html"

    def get_c_attach_items_mobile(self):
        if self.is_photo_list_attached():
            return "mobile/generic/attach/c_photo_list_attach.html"
        elif self.is_playlist_attached():
            return "mobile/generic/attach/c_playlist_attach.html"
        elif self.is_video_list_attached():
            return "mobile/generic/attach/c_video_list_attach.html"
        elif self.is_good_list_attached():
            return "mobile/generic/attach/c_good_list_attach.html"
        elif self.is_doc_list_attached():
            return "mobile/generic/attach/c_doc_list_attach.html"
        else:
            return "mobile/generic/attach/c_post_attach.html"

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
            return "desctop/posts/post_community/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "desctop/posts/post_community/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "desctop/generic/parent_attach/c_photo_list_attach.html"
        elif parent.is_good_repost():
            return "desctop/posts/post_community/good_repost.html"
        elif parent.is_good_list_repost():
            return "desctop/posts/post_community/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "desctop/generic/parent_attach/c_good_list_attach.html"
        elif parent.is_music_repost():
            return "desctop/posts/post_community/music_repost.html"
        elif parent.is_music_list_repost():
            return "desctop/posts/post_community/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "desctop/generic/parent_attach/c_playlist_attach.html"
        elif parent.is_video_repost():
            return "desctop/posts/post_community/video_repost.html"
        elif parent.is_video_list_repost():
            return "desctop/posts/post_community/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "desctop/generic/parent_attach/c_video_list_attach.html"
        elif parent.is_doc_repost():
            return "desctop/posts/post_community/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "desctop/posts/post_community/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "desctop/generic/parent_attach/c_doc_list_attach.html"
        elif parent.is_user_repost():
            return "desctop/posts/post_community/user_repost.html"
        elif parent.is_community_repost():
            return "desctop/posts/post_community/community_repost.html"
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
            return "desctop/posts/post_user/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "desctop/posts/post_user/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "desctop/generic/parent_attach/u_photo_list_attach.html"
        elif parent.is_good_repost():
            return "desctop/posts/post_user/good_repost.html"
        elif parent.is_good_list_repost():
            return "desctop/posts/post_user/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "desctop/generic/parent_attach/u_good_list_attach.html"
        elif parent.is_music_repost():
            return "desctop/posts/post_user/music_repost.html"
        elif parent.is_music_list_repost():
            return "desctop/posts/post_user/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "desctop/generic/parent_attach/u_playlist_attach.html"
        elif parent.is_video_repost():
            return "desctop/posts/post_user/video_repost.html"
        elif parent.is_video_list_repost():
            return "desctop/posts/post_user/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "desctop/generic/parent_attach/u_video_list_attach.html"
        elif parent.is_doc_repost():
            return "desctop/posts/post_user/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "desctop/posts/post_user/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "desctop/generic/parent_attach/u_doc_list_attach.html"
        elif parent.is_user_repost():
            return "desctop/posts/post_user/user_repost.html"
        elif parent.is_community_repost():
            return "desctop/posts/post_user/community_repost.html"
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
            return "mobile/posts/post_community/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "mobile/posts/post_community/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "mobile/generic/parent_attach/c_photo_list_attach.html"
        elif parent.is_good_repost():
            return "mobile/posts/post_community/good_repost.html"
        elif parent.is_good_list_repost():
            return "mobile/posts/post_community/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "mobile/generic/parent_attach/c_good_list_attach.html"
        elif parent.is_music_repost():
            return "mobile/posts/post_community/music_repost.html"
        elif parent.is_music_list_repost():
            return "mobile/posts/post_community/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "mobile/generic/parent_attach/c_playlist_attach.html"
        elif parent.is_video_repost():
            return "mobile/posts/post_community/video_repost.html"
        elif parent.is_video_list_repost():
            return "mobile/posts/post_community/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "mobile/generic/parent_attach/c_video_list_attach.html"
        elif parent.is_doc_repost():
            return "mobile/posts/post_community/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "mobile/posts/post_community/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "mobile/generic/parent_attach/c_doc_list_attach.html"
        elif parent.is_user_repost():
            return "mobile/posts/post_community/user_repost.html"
        elif parent.is_community_repost():
            return "mobile/posts/post_community/community_repost.html"
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
            return "mobile/posts/post_user/photo_repost.html"
        elif parent.is_photo_album_repost():
            return "mobile/posts/post_user/photo_album_repost.html"
        if parent.is_photo_list_attached():
            return "mobile/generic/parent_attach/u_photo_list_attach.html"
        elif parent.is_good_repost():
            return "mobile/posts/post_user/good_repost.html"
        elif parent.is_good_list_repost():
            return "mobile/posts/post_user/good_list_repost.html"
        elif parent.is_good_list_attached():
            return "mobile/generic/parent_attach/u_good_list_attach.html"
        elif parent.is_music_repost():
            return "mobile/posts/post_user/music_repost.html"
        elif parent.is_music_list_repost():
            return "mobile/posts/post_user/music_list_repost.html"
        elif parent.is_playlist_attached():
            return "mobile/generic/parent_attach/u_playlist_attach.html"
        elif parent.is_video_repost():
            return "mobile/posts/post_user/video_repost.html"
        elif parent.is_video_list_repost():
            return "mobile/posts/post_user/video_list_repost.html"
        elif parent.is_video_list_attached():
            return "mobile/generic/parent_attach/u_video_list_attach.html"
        elif parent.is_doc_repost():
            return "mobile/posts/post_user/doc_repost.html"
        elif parent.is_doc_list_repost():
            return "mobile/posts/post_user/doc_list_repost.html"
        elif parent.is_doc_list_attached():
            return "mobile/generic/parent_attach/u_doc_list_attach.html"
        elif parent.is_user_repost():
            return "mobile/posts/post_user/user_repost.html"
        elif parent.is_community_repost():
            return "mobile/posts/post_user/community_repost.html"
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


    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def count_comments(self):
        parent_comments = PostComment.objects.filter(post_id=self.pk)
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

    def get_fixed_for_user(self, user_id):
        try:
            item = Post.objects.get(creator_id=user_id, is_fixed=True, community=None)
            item.is_fixed = False
            item.save(update_fields=['is_fixed'])
            new_fixed = Post.objects.get(pk=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])
        except:
            new_fixed = Post.objects.get(pk=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])

    def get_fixed_for_community(self, community_id):
        try:
            item = Post.objects.get(community_id=community_id, is_fixed=True)
            item.is_fixed = False
            item.save(update_fields=['is_fixed'])
            new_fixed = Post.objects.get(pk=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])
        except:
            new_fixed = Post.objects.get(community_id=community_id,id=self.pk)
            new_fixed.is_fixed = True
            new_fixed.save(update_fields=['is_fixed'])

    def likes(self):
        likes = PostVotes.objects.filter(parent=self, vote__gt=0)
        return likes

    def dislikes(self):
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes

    def likes_count(self):
	    count = PostVotes.objects.filter(parent=self, vote__gt=0).values("pk").count()
	    if count > 0:
		    return count
	    else:
		    return ''

    def dislikes_count(self):
	    count = PostVotes.objects.filter(parent=self, vote__lt=0).values("pk").count()
	    if count > 0:
		    return count
	    else:
		    return ''

    def window_likes(self):
        likes = PostVotes.objects.filter(parent=self, vote__gt=0)
        return likes[0:6]

    def window_dislikes(self):
        dislikes = PostVotes.objects.filter(parent=self, vote__lt=0)
        return dislikes[0:6]

    def get_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents

    def get_window_reposts(self):
        parents = Post.objects.filter(parent=self)
        return parents[0:6]

    def count_reposts(self):
        parents = self.get_reposts()
        count_reposts = parents.count()
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
        count = UserLocation.objects.filter(user_id__in=ids, city_ru=sity).count()
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
        return self.replies.count()

    def likes(self):
        likes = PostCommentVotes.objects.filter(item=self, vote__gt=0)
        return likes

    def window_likes(self):
        likes = PostCommentVotes.objects.filter(item=self, vote__gt=0)
        return likes[0:6]

    def dislikes(self):
        dislikes = PostCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes

    def likes_count(self):
	    likes = PostCommentVotes.objects.filter(item=self, vote__gt=0).values("pk").count()
	    if likes > 0:
		    return likes
	    else:
		    return ''

    def dislikes_count(self):
	    dislikes = PostCommentVotes.objects.filter(item=self, vote__lt=0).values("pk").count()
	    if dislikes > 0:
		    return dislikes
	    else:
		    return ''

    def window_dislikes(self):
        dislikes = PostCommentVotes.objects.filter(item=self, vote__lt=0)
        return dislikes[0:6]

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
        comment.save()
        return comment

    def count_replies_ru(self):
        count = self.replies.count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

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

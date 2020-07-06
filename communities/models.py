import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models import Q
from pilkit.processors import ResizeToFill, ResizeToFit
from communities.helpers import upload_to_community_avatar_directory, upload_to_community_cover_directory
from imagekit.models import ProcessedImageField
from notifications.model.user import *
from rest_framework.exceptions import PermissionDenied


class CommunityCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    avatar = models.ImageField(blank=True, verbose_name="Аватар")
    order = models.IntegerField(default=0, verbose_name="Номер")

    def __str__(self):
        return 'Категория: ' + self.name

    class Meta:
        verbose_name="Категория сообществ"
        verbose_name_plural="Категории сообществ"


class CommunitySubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    sudcategory = models.ForeignKey(CommunityCategory, on_delete=models.CASCADE, related_name='community_categories', verbose_name="Подкатегория сообщества")
    avatar = models.ImageField(blank=True, verbose_name="Аватар")
    order = models.IntegerField(default=0, verbose_name="Номер")

    def __str__(self):
        return 'ПодКатегория: ' + self.name

    class Meta:
        verbose_name="Подкатегория сообществ"
        verbose_name_plural="Подкатегории сообществ"


class Community(models.Model):
    category = models.ForeignKey(CommunitySubCategory, on_delete=models.CASCADE, related_name='community_sub_categories', verbose_name="Подкатегория сообщества")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_communities', null=False, blank=False, verbose_name="Создатель")
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Название" )
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Описание" )
    rules = models.TextField(max_length=1000, blank=True, null=True, verbose_name="Правила")
    cover = ProcessedImageField(blank=True, format='JPEG',options={'quality': 90},upload_to=upload_to_community_avatar_directory,processors=[ResizeToFit(width=1024, upscale=False)])
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")
    banned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='banned_of_communities', verbose_name="Черный список")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    COMMUNITY_TYPE_PRIVATE = 'T'
    COMMUNITY_TYPE_PUBLIC = 'P'
    COMMUNITY_TYPE_CLOSED = 'C'
    COMMUNITY_TYPES = (
        (COMMUNITY_TYPE_PUBLIC, 'Публичное'),
        (COMMUNITY_TYPE_PRIVATE, 'Приватное'),
        (COMMUNITY_TYPE_CLOSED, 'Закрытое'),
    )
    type = models.CharField(choices=COMMUNITY_TYPES, default='P', max_length=2)
    invites_enabled = models.BooleanField(default=True, verbose_name="Разрешить приглашения")
    is_deleted = models.BooleanField(default=False,verbose_name="Удаленное")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="uuid")
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_community_avatar_directory)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_community_avatar_directory)

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'сообщества'

    def get_avatar_uuid(self):
        avatar = self.get_avatar_photos().order_by('-id')[0]
        return avatar.uuid

    def create_s_avatar(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer

        self.s_avatar = photo_input
        self.save(update_fields=['s_avatar'])
        new_img = get_thumbnailer(self.s_avatar)['small_avatar'].url.replace('media/', '')
        self.s_avatar = new_img
        self.save(update_fields=['s_avatar'])
        return self.s_avatar

    def create_b_avatar(self, photo_input):
        from easy_thumbnails.files import get_thumbnailer

        self.b_avatar = photo_input
        self.save(update_fields=['b_avatar'])
        new_img = get_thumbnailer(self.b_avatar)['avatar'].url.replace('media/', '')
        self.b_avatar = new_img
        self.save(update_fields=['b_avatar'])
        return self.b_avatar

    def get_b_avatar(self):
        try:
            return self.b_avatar.url
        except:
            return None

    def get_avatar(self):
        try:
            return self.s_avatar.url
        except:
            return None

    @classmethod
    def create_community(cls, name, category, creator, type, description=None, rules=None, invites_enabled=None):
        from music.models import SoundList
        from video.models import VideoAlbum

        if type is Community.COMMUNITY_TYPE_PRIVATE and invites_enabled is None:
            invites_enabled = False
        else:
            invites_enabled = True
        community = cls.objects.create(name=name, creator=creator, description=description, type=type, rules=rules, invites_enabled=invites_enabled, category=category)
        CommunityMembership.create_membership(user=creator, is_administrator=True, is_advertiser=False, is_editor=False, is_moderator=False, community=community)
        community.save()
        SoundList.objects.create(creator=creator, community_id=community.pk, is_generic=True, name="Основной плейлист")
        VideoAlbum.objects.create(creator=creator, community_id=community.pk, is_generic=True, title="Все видео")
        return community

    @classmethod
    def is_user_with_username_member_of_community_with_name(cls, username, community_name):
        return cls.objects.filter(name=community_name, memberships__user__username=username).exists()

    @classmethod
    def is_user_with_username_administrator_of_community_with_name(cls, user_id, community_name):
        return cls.objects.filter(name=community_name, memberships__user__id=user_id, memberships__is_administrator=True).exists()

    @classmethod
    def is_user_with_username_moderator_of_community_with_name(cls, username, community_name):
        return cls.objects.filter(name=community_name, memberships__user__username=username, memberships__is_moderator=True).exists()

    @classmethod
    def is_user_with_username_banned_from_community_with_name(cls, username, community_name):
        return cls.objects.filter(name=community_name, banned_users__username=username).exists()

    @classmethod
    def is_community_with_name_invites_enabled(cls, community_name):
        return cls.objects.filter(name=community_name, invites_enabled=True).exists()

    @classmethod
    def is_community_with_name_private(cls, community_name):
        return cls.objects.filter(name=community_name, type='T').exists()

    @classmethod
    def is_community_with_name_closed(cls, community_name):
        return cls.objects.filter(name=community_name, type='C').exists()

    @classmethod
    def get_community_with_name_for_user_with_id(cls, community_name, user_id):
        query = Q(name=community_name, is_deleted=False)
        query.add(~Q(banned_users__id=user_id), Q.AND)
        return cls.objects.get(query)

    @classmethod
    def search_communities_with_query(cls, query):
        query = cls._make_search_communities_query(query=query)
        return cls.objects.filter(query)

    @classmethod
    def _make_search_communities_query(cls, query):
        communities_query = Q(name__icontains=query)
        communities_query.add(Q(title__icontains=query), Q.OR)
        communities_query.add(Q(is_deleted=False), Q.AND)
        return communities_query

    @classmethod
    def get_trending_communities_for_user_with_id(cls, user_id, category_name=None):
        trending_communities_query = cls._make_trending_communities_query(category_name=category_name)
        trending_communities_query.add(~Q(banned_users__id=user_id), Q.AND)
        return cls._get_trending_communities_with_query(query=trending_communities_query)

    def get_posts(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        posts_query = Q(community_id=self.pk, is_deleted=False, is_fixed=False, status=Post.STATUS_PUBLISHED)
        exclude_moderated_posts_query = ~Q(moderated_post__status=ModeratedPost.STATUS_SUSPEND)
        posts_query.add(exclude_moderated_posts_query, Q.AND)
        posts = Post.objects.filter(posts_query)
        return posts
    def get_draft_posts(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        posts_query = Q(community_id=self.pk, is_deleted=False, is_fixed=False, status=Post.STATUS_DRAFT)
        exclude_moderated_posts_query = ~Q(moderated_post__status=ModeratedPost.STATUS_SUSPEND)
        posts_query.add(exclude_moderated_posts_query, Q.AND)
        posts = Post.objects.filter(posts_query)
        return posts
    def get_archive_posts(self):
        from posts.models import Post
        from managers.model.post import ModeratedPost

        posts_query = Q(community_id=self.pk, is_deleted=False, is_fixed=False, status=Post.STATUS_ARHIVED)
        exclude_moderated_posts_query = ~Q(moderated_post__status=ModeratedPost.STATUS_SUSPEND)
        posts_query.add(exclude_moderated_posts_query, Q.AND)
        posts = Post.objects.filter(posts_query)
        return posts

    def get_goods(self):
        from goods.models import Good

        goods_query = Q(community_id=self.pk, is_deleted=False, status=Good.STATUS_PUBLISHED)
        #exclude_reported_and_approved_goods_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #goods_query.add(exclude_reported_and_approved_goods_query, Q.AND)
        goods = Good.objects.filter(goods_query)
        return goods
    def get_admin_goods(self):
        from goods.models import Good

        goods_query = Q(community_id=self.pk, is_deleted=False)
        #exclude_reported_and_approved_goods_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #goods_query.add(exclude_reported_and_approved_goods_query, Q.AND)
        goods = Good.objects.filter(goods_query)
        return goods

    def get_photos_for_album(self, album_id):
        from gallery.models import Photo

        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        photos_query = Q(is_deleted=False, album__pk=album_id, is_public=True)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos
    def get_photos_for_admin_album(self, album_id):
        from gallery.models import Photo

        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        photos_query = Q(is_deleted=False, album_id=album_id)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos

    def get_photos(self):
        from gallery.models import Photo

        photos_query = Q(is_deleted=False, is_public=True, community=self)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos
    def get_admin_photos(self):
        from gallery.models import Photo

        photos_query = Q(is_deleted=False, community=self)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos

    def get_avatar_photos(self):
        from gallery.models import Photo

        photos_query = Q(is_deleted=False, album__title="Фото со страницы", album__is_generic=True, album__community=self)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        avatar_photos = Photo.objects.filter(photos_query)
        return avatar_photos

    def get_albums(self):
        from gallery.models import Album

        albums_query = Q(community=self, is_deleted=False, is_public=True)
        #exclude_reported_and_approved_albums_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #albums_query.add(exclude_reported_and_approved_albums_query, Q.AND)
        albums = Album.objects.filter(albums_query)
        return albums

    def is_album_exists(self):
        return self.album_community.filter(community=self, is_deleted=False).exists()

    def count_photos(self):
        return self.photo_community.values('is_deleted').filter(is_deleted=False).count()

    def get_profile_photos(self):
        from gallery.models import Photo

        photos_query = Q(community=self, is_deleted=False, is_public=True)
        #exclude_reported_and_approved_photos_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #photos_query.add(exclude_reported_and_approved_photos_query, Q.AND)
        photos = Photo.objects.filter(photos_query)
        return photos[0:6]

    def get_admin_albums(self):
        from gallery.models import Album

        albums_query = Q(is_deleted=False, community=None)
        #exclude_reported_and_approved_albums_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        #albums_query.add(exclude_reported_and_approved_albums_query, Q.AND)
        albums = Album.objects.filter(albums_query)
        return albums

    def get_music(self):
        from music.models import SoundList, SoundcloudParsing

        #exclude_reported_and_approved_music_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        list = SoundList.objects.get(community=self, is_generic=True, name="Основной плейлист")
        music_query = Q(list=list, is_deleted=False)
        #music_query.add(exclude_reported_and_approved_music_query, Q.AND)
        music_list = SoundcloudParsing.objects.filter(music_query)
        return music_list

    def get_last_music(self):
        from music.models import SoundList, SoundcloudParsing

        #exclude_reported_and_approved_music_query = ~Q(moderated_object__status=ModeratedObject.STATUS_APPROVED)
        list = SoundList.objects.get(community=self, is_generic=True, name="Основной плейлист")
        music_query = Q(list=list, is_deleted=False)
        #music_query.add(exclude_reported_and_approved_music_query, Q.AND)
        music_list = SoundcloudParsing.objects.filter(music_query)
        return music_list[0:5]

    def get_music_list_id(self):
        from music.models import SoundList

        list = SoundList.objects.get(community_id=self.pk, is_generic=True, name="Основной плейлист")
        return list.pk

    def get_last_video(self):
        from video.models import Video, VideoAlbum
        try:
            list = VideoAlbum.objects.get(community_id=self.pk, is_generic=True, title="Все видео")
            video_query = Q(album=list, is_deleted=False, is_public=True)
            video_list = Video.objects.filter(video_query).order_by("-created")
            return video_list[0:2]
        except:
            return None

    def get_template(self, folder, template, request):
        import re

        if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.name):
            if request.user.is_administrator_of_community_with_name(self.name):
                template_name = folder + "admin_" + template
            elif request.user.is_moderator_of_community_with_name(self.name):
                template_name = folder + "moderator_" + template
            elif request.user.is_editor_of_community_with_name(self.name):
                template_name = folder + "editor_" + template
            elif request.user.is_advertiser_of_community_with_name(self.name):
                template_name = folder + "advertiser_" + template
            else:
                template_name = folder + "member_" + template
        elif request.user.is_authenticated and request.user.is_follow_from_community_with_name(self.pk):
            template_name = folder + "follow_" + template
        elif request.user.is_authenticated and request.user.is_banned_from_community_with_name(self.name):
            template_name = folder + "block_" + template

        elif request.user.is_authenticated and self.is_public():
            template_name = folder + "public_" + template
        elif request.user.is_authenticated and self.is_closed():
            template_name = folder + "close_" + template
        elif request.user.is_authenticated and self.is_private():
            template_name = folder + "private_" + template

        elif request.user.is_anonymous and self.is_public():
            template_name = folder + "anon_public_" + template
        elif self.is_closed and request.user.is_anonymous():
            template_name = folder + "anon_close_" + template
        elif request.user.is_anonymous and self.is_private():
            template_name = folder + "anon_private_" + template

        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    def get_manage_template(self, folder, template, request):
        import re

        if request.user.is_administrator_of_community_with_name(self.name):
            template_name = folder + template
        else:
            raise PermissionDenied('Ошибка доступа.')
        MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    def get_moders_template(self, folder, template, request):
        import re

        if request.user.is_administrator_of_community_with_name(self.name) or request.user.is_moderator_of_community_with_name(self.name):
            template_name = folder + template
        else:
            raise PermissionDenied('Ошибка доступа.')
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    def get_template_list(self, folder, template, request):
        import re

        if request.user.is_authenticated and request.user.is_member_of_community_with_name(self.name):
            if request.user.is_moderator_of_community_with_name(self.name):
                template_name = folder + "moderator_" + template
            elif request.user.is_administrator_of_community_with_name(self.name):
                template_name = folder + "admin_" + template
            elif request.user.is_editor_of_community_with_name(self.name):
                template_name = folder + "admin_" + template
            else:
                template_name = folder + template
        elif request.user.is_authenticated and self.is_public():
            template_name = folder + template
        elif request.user.is_anonymous and self.is_public():
            template_name = folder + "anon_" + template
        MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            template_name = "mob_" + template_name
        return template_name

    @classmethod
    def get_trending_communities(cls, category_name=None):
        trending_communities_query = cls._make_trending_communities_query(category_name=category_name)
        return cls._get_trending_communities_with_query(query=trending_communities_query)

    @classmethod
    def _get_trending_communities_with_query(cls, query):
        from django.db.models import Count

        return cls.objects.annotate(Count('memberships')).filter(query).order_by('-memberships__count', '-created')

    @classmethod
    def _make_trending_communities_query(cls, category_name=None):
        trending_communities_query = Q(is_deleted=False)
        if category_name:
            trending_communities_query.add(Q(categories__name=category_name), Q.AND)
        return trending_communities_query


    @classmethod
    def get_community_with_name_members(cls, community_name):
        from users.models import User

        community_members_query = Q(communities_memberships__community__name=community_name)
        return User.objects.filter(community_members_query)

    @classmethod
    def get_community_with_name_administrators(cls, community_name):
        from users.models import User

        community_administrators_query = Q(communities_memberships__community__name=community_name, communities_memberships__is_administrator=True)
        return User.objects.filter(community_administrators_query)

    @classmethod
    def get_community_with_name_moderators(cls, community_name):
        from users.models import User

        community_administrators_query = Q(communities_memberships__community__name=community_name, communities_memberships__is_moderator=True)
        return User.objects.filter(community_administrators_query)

    @classmethod
    def get_community_with_name_editors(cls, community_name):
        from users.models import User

        community_moderators_query = Q(communities_memberships__community__name=community_name, communities_memberships__is_editor=True)
        return User.objects.filter(community_moderators_query)

    @classmethod
    def get_community_with_name_advertisers(cls, community_name):
        from users.models import User

        community_moderators_query = Q(communities_memberships__community__name=community_name, communities_memberships__is_advertiser=True)
        return User.objects.filter(community_moderators_query)

    @classmethod
    def get_community_with_name_follows(cls, community_name):
        from users.models import User

        community_moderators_query = Q(communities_memberships__community__name=community_name, communities_memberships__is_moderator=True)
        return User.objects.filter(community_moderators_query)

    @classmethod
    def get_community_with_name_banned_users(cls, community_name):
        community = Community.objects.get(name=community_name)
        community_members_query = Q()
        return community.banned_users.filter(community_members_query)

    @classmethod
    def search_community_with_name_members(cls, community_name, query):
        from users.models import User

        db_query = Q(communities_memberships__community__name=community_name)
        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)
        db_query.add(community_members_query, Q.AND)
        return User.objects.filter(db_query)

    @classmethod
    def search_community_with_name_moderators(cls, community_name, query):
        from users.models import User

        db_query = Q(communities_memberships__community__name=community_name, communities_memberships__is_moderator=True)
        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)
        db_query.add(community_members_query, Q.AND)
        return User.objects.filter(db_query)

    @classmethod
    def search_community_with_name_administrators(cls, community_name, query):
        from users.models import User

        db_query = Q(communities_memberships__community__name=community_name, communities_memberships__is_administrator=True)
        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)
        db_query.add(community_members_query, Q.AND)
        return User.objects.filter(db_query)

    @classmethod
    def search_community_with_name_banned_users(cls, community_name, query):
        community = Community.objects.get(name=community_name)
        community_banned_users_query = Q(username__icontains=query)
        community_banned_users_query.add(Q(profile__name__icontains=query), Q.OR)
        return community.banned_users.filter(community_banned_users_query)

    def get_staff_members(self):
        from users.models import User

        staff_members_query = Q(communities_memberships__community_id=self.pk)
        staff_members_query.add(Q(communities_memberships__is_administrator=True) | Q(communities_memberships__is_moderator=True) | Q(communities_memberships__is_advertiser=True) | Q(communities_memberships__is_editor=True), Q.AND)
        return User.objects.filter(staff_members_query)

    def is_private(self):
        return self.type is self.COMMUNITY_TYPE_PRIVATE

    def is_closed(self):
        return self.type is self.COMMUNITY_TYPE_CLOSED

    def is_public(self):
        return self.type is self.COMMUNITY_TYPE_PUBLIC

    def is_community_playlist(self):
        from music.models import UserTempSoundList
        try:
            UserTempSoundList.objects.get(tag=None, community=self, genre=None)
            return True
        except:
            return False

    def add_administrator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = True
        user_membership.is_editor = False
        user_membership.is_advertiser = False
        user_membership.save()
        return user_membership
    def add_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = True
        user_membership.is_administrator = False
        user_membership.is_editor = False
        user_membership.is_advertiser = False
        user_membership.save()
        return user_membership
    def add_editor(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = False
        user_membership.is_editor = True
        user_membership.is_advertiser = False
        user_membership.save()
        return user_membership
    def add_advertiser(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = False
        user_membership.is_editor = False
        user_membership.is_advertiser = True
        user_membership.save()
        return user_membership

    def remove_administrator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_administrator = False
        user_membership.save(update_fields=['is_administrator'])
        return user_membership
    def remove_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.save(update_fields=['is_moderator'])
        return user_membership
    def remove_editor(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_editor = False
        user_membership.save(update_fields=['is_editor'])
        return user_membership
    def remove_advertiser(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_advertiser = False
        user_membership.save(update_fields=['is_advertiser'])
        return user_membership

    def add_member(self, user):
        user_membership = CommunityMembership.create_membership(user=user, community=self)
        return user_membership

    def remove_member(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.delete()

    def notification_new_member(self, user):
        community_notification_handler(actor=user, recipient=None, verb=UserCommunityNotification.JOIN, community=self.community, key='notification')

    def create_invite(self, creator, invited_user):
        from invitations.models import CommunityInvite

        CommunityInvite = get_community_invite_model()
        return CommunityInvite.create_community_invite(creator=creator, invited_user=invited_user, community=self)

    def __str__(self):
        return self.name

    def count_members(self):
        return self.memberships.count()

    def get_sity_count(self, sity):
        from stst.models import CommunityNumbers
        from users.model.profile import OneUserLocation

        v_s = CommunityNumbers.objects.filter(community=self.pk).values('user')
        ids = [use['user'] for use in v_s]
        count = OneUserLocation.objects.filter(user_id__in=ids, city_ru=sity).count()
        return count


    ''''' модерация '''''
    def get_longest_community_penalties(self):
        return self.community_penalties.filter(community=self)[0].expiration
    def get_moderated_description(self):
        return self.moderated_community.filter(community=self)[0].description
    def is_suspended(self):
        return self.community_penalties.filter(type="S", expiration__gt=timezone.now()).exists()
    def is_blocked(self):
        return self.community_penalties.filter(type="B").exists()
    def is_have_warning_banner(self):
        return self.community_penalties.filter(type="BA").exists()

    ''''' конец модерации '''''


class CommunityMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='communities_memberships', null=False, blank=False, verbose_name="Члены сообщества")
    community = models.ForeignKey(Community, db_index=False, on_delete=models.CASCADE, related_name='memberships', null=False, blank=False, verbose_name="Сообщество")
    is_administrator = models.BooleanField(default=False, verbose_name="Это администратор")
    is_moderator = models.BooleanField(default=False, verbose_name="Это модератор")
    is_editor = models.BooleanField(default=False, verbose_name="Это редактор")
    is_advertiser = models.BooleanField(default=False, verbose_name="Это рекламодатель")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создано")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_membership(cls, user, community, is_administrator=False, is_editor=False, is_advertiser=False, is_moderator=False):
        membership = cls.objects.create(user=user, community=community, is_administrator=is_administrator, is_editor=is_editor, is_advertiser=is_advertiser, is_moderator=is_moderator)
        return membership

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(CommunityMembership, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('user', 'community'),)
        indexes = [
            models.Index(fields=['community', 'user']),
            models.Index(fields=['community', 'user', 'is_administrator']),
            models.Index(fields=['community', 'user', 'is_moderator']),
            models.Index(fields=['community', 'user', 'is_editor']),
            models.Index(fields=['community', 'user', 'is_advertiser']),
            ]
        verbose_name = 'подписчик сообщества'
        verbose_name_plural = 'подписчики сообщества'


class CommunityLog(models.Model):
    source_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', null=False, blank=False, verbose_name="Кто модерирует")
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=False, verbose_name="Кого модерируют")
    item = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='+', null=True, blank=True, verbose_name="Пост")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='logs', null=False, blank=False, verbose_name="Сообщество")
    created = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Создан")

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

    @classmethod
    def create_community_log(cls, community, action_type, source_user, target_user, item=None):
        return cls.objects.create(community=community, action_type=action_type, source_user=source_user,
                                  target_user=target_user, item=item)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(CommunityLog, self).save(*args, **kwargs)


class CommunityInvite(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='created_communities_invites', null=False,blank=False, verbose_name="Кто приглашает в сообщество")
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='communities_invites', null=False, blank=False, verbose_name="Кого приглашают в сообщество")
    community = models.ForeignKey(Community, db_index=False, on_delete=models.CASCADE, related_name='invites', null=False, blank=False, verbose_name="Сообщество")

    @classmethod
    def create_community_invite(cls, creator, invited_user, community):
        return cls.objects.create(creator=creator, invited_user=invited_user, community=community)

    @classmethod
    def is_user_with_username_invited_to_community_with_name(cls, username, community_name):
        return cls.objects.filter(community__name=community_name, invited_user__username=username).exists()

    class Meta:
        unique_together = (('invited_user', 'community', 'creator'),)
        verbose_name = 'Приглашение в сообщество'
        verbose_name_plural = 'Приглашения в сообщества'

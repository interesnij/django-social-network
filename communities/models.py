import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q
from pilkit.processors import ResizeToFill, ResizeToFit
from communities.helpers import upload_to_community_avatar_directory, upload_to_community_cover_directory
from imagekit.models import ProcessedImageField
from common.utils import try_except
from django.contrib.postgres.indexes import BrinIndex


class CommunityCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    avatar = models.ImageField(blank=True, verbose_name="Аватар")
    order = models.IntegerField(default=0, verbose_name="Номер")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Категория сообществ"
        verbose_name_plural="Категории сообществ"
        ordering = ["order"]


class CommunitySubCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    sudcategory = models.ForeignKey(CommunityCategory, on_delete=models.CASCADE, related_name='community_categories', verbose_name="Категория сообщества")
    avatar = models.ImageField(blank=True, verbose_name="Аватар")
    order = models.IntegerField(default=0, verbose_name="Номер")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Подкатегория сообществ"
        verbose_name_plural="Подкатегории сообществ"
        ordering = ["order"]


class Community(models.Model):
    COMMUNITY_TYPE_PRIVATE = 'T'
    COMMUNITY_TYPE_PUBLIC = 'P'
    COMMUNITY_TYPE_CLOSED = 'C'
    COMMUNITY_TYPES = (
        (COMMUNITY_TYPE_PUBLIC, 'Публичное'),
        (COMMUNITY_TYPE_PRIVATE, 'Приватное'),
        (COMMUNITY_TYPE_CLOSED, 'Закрытое'),
    )
    DELETED = 'DE'
    BLOCKED = 'BL'
    CHILD = 'CH'
    STANDART = 'ST'
    VERIFIED_SEND = 'VS'
    VERIFIED = 'VE'
    PERM = (
        (DELETED, 'Удален'),
        (BLOCKED, 'Заблокирован'),
        (CHILD, 'Детская'),
        (STANDART, 'Обычные права'),
        (VERIFIED_SEND, 'Запрос на проверку'),
        (VERIFIED, 'Провернный'),
    )

    category = models.ForeignKey(CommunitySubCategory, on_delete=models.CASCADE, related_name='community_sub_categories', verbose_name="Подкатегория сообщества")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_communities', null=False, blank=False, verbose_name="Создатель")
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Название" )
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name="Описание" )
    cover = ProcessedImageField(blank=True, format='JPEG',options={'quality': 90},upload_to=upload_to_community_avatar_directory,processors=[ResizeToFit(width=1024, upscale=False)])
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    banned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='banned_of_communities', verbose_name="Черный список")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    type = models.CharField(choices=COMMUNITY_TYPES, default='P', max_length=2)
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_community_cover_directory)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_community_cover_directory)
    perm = models.CharField(max_length=5, choices=PERM, default=STANDART, verbose_name="Уровень доступа")
    have_link = models.CharField(max_length=17, blank=True, verbose_name='Ссылка')
    invites_enabled = models.BooleanField(default=True, verbose_name="Приглашения открыты")

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'сообщества'
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.name

    def create_banned_user(self, user):
        self.banned_users.add(user)
        self.remove_member(user)
        self.delete_notify_subscriber(user.pk)
        return True
    def delete_banned_user(self, user):
        self.banned_users.remove(user)
        return True

    def get_posts_ids(self):
        from posts.models import Post
        posts = Post.objects.filter(list__in=self.get_admin_all_post_lists()).values('id')
        return [i['id'] for i in posts]

    def get_community_avatar(self):
        if self.s_avatar:
            return '<img style="border-radius:50px;width:50px;" alt="image" src="' + self.s_avatar.url + ' />'
        else:
            return '<svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"></path></svg>'

    def get_slug(self):
        if self.have_link:
            return "@" + self.have_link
        else:
            return "@public" + str(self.pk)
    def get_link(self):
        if self.have_link:
            return "/" + self.have_link + "/"
        else:
            return "/public" + str(self.pk) + "/"

    def is_deleted(self):
        return try_except(self.perm == Community.DELETED)
    def is_standart(self):
        return try_except(self.perm == Community.STANDART)
    def is_verified_send(self):
        return try_except(self.perm == Community.VERIFIED_SEND)
    def is_verified(self):
        return try_except(self.perm == Community.VERIFIED)
    def is_child(self):
        return try_except(self.perm == Community.CHILD)

    def is_photo_open(self):
        return try_except(self.community_sections_open.photo)
    def is_good_open(self):
        return try_except(self.community_sections_open.good)
    def is_video_open(self):
        return try_except(self.community_sections_open.video)
    def is_music_open(self):
        return try_except(self.community_sections_open.music)
    def is_doc_open(self):
        return try_except(self.community_sections_open.doc)
    def is_link_open(self):
        return try_except(self.community_sections_open.link)
    def is_article_open(self):
        return try_except(self.community_sections_open.article)
    def is_contacts_open(self):
        return try_except(self.community_sections_open.contacts)
    def is_discussion_open(self):
        return try_except(self.community_sections_open.discussion)

    @classmethod
    def create_community(cls, name, category, creator, type, description=None, invites_enabled=None):
        from common.processing.community import create_community_models
        if type is Community.COMMUNITY_TYPE_PRIVATE and invites_enabled is None:
            invites_enabled = False
        else:
            invites_enabled = True
        community = cls.objects.create(name=name, creator=creator, description=description, type=type, invites_enabled=invites_enabled, category=category)
        CommunityMembership.create_membership(user=creator, is_administrator=True, is_advertiser=False, is_editor=False, is_moderator=False, community=community)
        community.save()
        creator.create_or_plus_populate_community(community.pk)
        community.add_news_subscriber(creator.pk)
        community.add_notify_subscriber(creator.pk)
        create_community_models(community)
        return community

    @classmethod
    def is_user_with_username_member_of_community(cls, username, community_pk):
        return cls.objects.filter(pk=community_pk, memberships__user__username=username).exists()

    @classmethod
    def is_user_with_username_administrator_of_community(cls, user_id, community_pk):
        return cls.objects.filter(pk=community_pk, memberships__user__id=user_id, memberships__is_administrator=True).exists()

    @classmethod
    def is_user_with_username_moderator_of_community(cls, username, community_pk):
        return cls.objects.filter(pk=community_pk, memberships__user__username=username, memberships__is_moderator=True).exists()

    @classmethod
    def is_user_with_username_banned_from_community(cls, username, community_pk):
        return cls.objects.filter(pk=community_pk, banned_users__username=username).exists()

    @classmethod
    def is_community_invites_enabled(cls, community_pk):
        return cls.objects.filter(pk=community_pk, invites_enabled=True).exists()

    @classmethod
    def is_community_private(cls, community_pk):
        return cls.objects.filter(pk=community_pk, type='T').exists()

    @classmethod
    def is_community_closed(cls, community_pk):
        return cls.objects.filter(pk=community_pk, type='C').exists()

    @classmethod
    def get_community_for_user_with_id(cls, community_pk, user_id):
        query = Q(pk=community_pk, is_deleted=False)
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

    def is_have_fixed_posts(self):
        from posts.models import PostList
        try:
            list = PostList.objects.get(community_id=self.pk, type=PostList.FIX)
            if list.is_not_empty():
                return True
            else:
                return False
        except:
            pass

    def get_or_create_fix_list(self):
        from posts.models import PostList
        try:
            return PostList.objects.get(community_id=self.pk, type=PostList.FIX)
        except:
            return PostList.objects.create(creator_id=self.creator.pk, community_id=self.pk, type=PostList.FIX, name="Закрепленный список")

    def get_posts(self):
        from posts.models import Post, PostList

        list = PostList.objects.get(community_id=self.id, type=PostList.MAIN)
        return Post.objects.filter(list=list, is_deleted=False)
    def get_draft_posts(self):
        from posts.models import Post, PostList

        posts_query = Q(community_id=self.pk, is_deleted=False, status=Post.STATUS_DRAFT)
        return Post.objects.filter(posts_query)
    def get_count_draft_posts(self):
        from posts.models import Post

        posts_query = Q(community_id=self.pk, is_deleted=False, status=Post.STATUS_DRAFT)
        return Post.objects.filter(posts_query).values("pk").count()

    def get_count_articles(self):
        from article.models import Article

        articles_query = Q(community_id=self.pk, is_deleted=False, status=Article.STATUS_DRAFT)
        return Article.objects.filter(articles_query).values("pk").count()

    def id_draft_posts_exists(self):
        from posts.models import Post

        posts_query = Q(community_id=self.pk, is_deleted=False, status=Post.STATUS_DRAFT)
        return Post.objects.filter(posts_query).exists()

    def get_draft_posts_for_user(self, user_pk):
        from posts.models import Post

        posts_query = Q(creator_id=user_pk, community_id=self.pk, is_deleted=False, status=Post.STATUS_DRAFT)
        return Post.objects.filter(posts_query)
    def get_count_draft_posts_for_user(self, user_pk):
        from posts.models import Post

        posts_query = Q(creator_id=user_pk, community_id=self.pk, is_deleted=False, status=Post.STATUS_DRAFT)
        return Post.objects.filter(posts_query).values("pk").count()

    def get_archive_posts(self):
        from posts.models import Post, PostList

        list = PostList.objects.get(community_id=self.id, type=PostList.DELETED)
        return Post.objects.filter(list=list, is_deleted=False)

    def get_post_lists(self):
        from posts.models import PostList
        lists_query = Q(community_id=self.id, is_deleted=False)
        lists_query.add(~Q(Q(type=PostList.DELETED)|Q(type=PostList.PRIVATE)|Q(type=PostList.FIX)), Q.AND)
        return PostList.objects.filter(lists_query)
    def get_admin_all_post_lists(self):
        from posts.models import PostList
        lists_query = Q(community_id=self.id, is_deleted=False)
        lists_query.add(~Q(Q(type=PostList.DELETED)|Q(type=PostList.FIX)), Q.AND)
        return PostList.objects.filter(lists_query)

    def get_count_photos(self):
        from gallery.models import Album
        albums, count = Album.objects.filter(community_id=self.id), 0
        for album in albums:
            count += album.count_photo()
        return count

    def get_albums(self):
        from gallery.models import Album

        albums_query = Q(is_deleted=False, is_public=True)
        albums_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        albums_query.add(~Q(type=Album.MAIN), Q.AND)
        return Album.objects.filter(albums_query).order_by("order")

    def count_albums(self):
        return self.album_community.filter(community_id=self.pk, is_deleted=False).values('pk').count()

    def get_admin_albums(self):
        from gallery.models import Album

        albums_query = Q(is_deleted=False)
        albums_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        albums_query.add(~Q(type=Album.MAIN), Q.AND)
        return Album.objects.filter(albums_query).order_by("order")

    def is_album_exists(self):
        from gallery.models import Album

        albums_query = Q(is_deleted=False, is_public=True)
        albums_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        albums_query.add(~Q(type=Album.MAIN), Q.AND)
        return Album.objects.filter(albums_query).exists()

    def get_profile_photos(self):
        return self.get_photos()[0:6]

    def is_good_album_exists(self):
        return self.good_album_community.filter(community_id=self.id, type="AL", is_deleted=False).exists()
    def get_good_albums(self):
        from goods.models import GoodAlbum

        albums_query = Q(community_id=self.id, type="AL", is_deleted=False)
        return GoodAlbum.objects.filter(albums_query).order_by("order")
    def get_all_good_albums(self):
        from goods.models import GoodAlbum

        albums_query = Q(community_id=self.id, is_deleted=False)
        return GoodAlbum.objects.filter(albums_query).order_by("order")

    def get_goods_count(self):
        count = 0
        for list in self.get_all_good_albums():
            count += list.count_goods()
        return count

    def get_or_create_good_album(self):
        from goods.models import GoodAlbum
        try:
            return GoodAlbum.objects.get(community_id=self.pk, type=GoodAlbum.MAIN)
        except:
            return GoodAlbum.objects.create(creator_id=self.creator.pk, community_id=self.pk, type=GoodAlbum.MAIN, title="Основной альбом")
    def get_or_create_playlist(self):
        from music.models import SoundList
        try:
            return SoundList.objects.get(community_id=self.pk, type=SoundList.MAIN)
        except:
            return SoundList.objects.create(creator_id=self.creator.pk, community_id=self.pk, type=SoundList.MAIN, name="Основной плейлист")
    def get_or_create_video_album(self):
        from video.models import VideoAlbum
        try:
            return VideoAlbum.objects.get(community_id=self.pk, type=VideoAlbum.MAIN)
        except:
            return VideoAlbum.objects.create(creator_id=self.creator.pk, community_id=self.pk, type=VideoAlbum.MAIN, title="Основной альбом")
    def get_or_create_photo_album(self):
        from gallery.models import Album
        try:
            return Album.objects.get(community_id=self.pk, type=Album.MAIN)
        except:
            return Album.objects.create(creator_id=self.creator.pk, community_id=self.pk, type=Album.MAIN, title="Основной альбом")
    def get_or_create_doc_list(self):
        from docs.models import DocList
        try:
            return DocList.objects.get(community_id=self.pk, type=DocList.MAIN)
        except:
            return DocList.objects.create(creator_id=self.creator.pk, community_id=self.pk, type=DocList.MAIN, name="Основной список")

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

    def get_music(self):
        from music.models import SoundList, SoundcloudParsing

        list = SoundList.objects.get(community=self, type=SoundList.MAIN)
        music_query = Q(list=list, is_deleted=False)
        return SoundcloudParsing.objects.filter(music_query)

    def get_music_count(self):
        from music.models import SoundList
        playlists, count = SoundList.objects.filter(community_id=self.id), 0
        for playlist in playlists:
            count += playlist.count_tracks()
        return count

    def get_last_music(self):
        from music.models import SoundList, SoundcloudParsing

        list = SoundList.objects.get(community=self, type=SoundList.MAIN)
        music_query = Q(list=list, is_deleted=False)
        return SoundcloudParsing.objects.filter(music_query)[0:5]

    def is_music_playlist_exists(self):
        from music.models import SoundList

        playlists_query = Q(type=SoundList.LIST, is_deleted=False)
        playlists_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        return SoundList.objects.filter(playlists_query).exists()

    def get_audio_playlists(self):
        from music.models import SoundList

        playlists_query = Q(type=SoundList.LIST, is_deleted=False)
        playlists_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        return SoundList.objects.filter(playlists_query).order_by("order")

    def get_docs(self):
        from docs.models import DocList, Doc

        list = DocList.objects.get(community=self, type=DocList.MAIN)
        docs_query = Q(list=list, is_deleted=False)
        return Doc.objects.filter(Doc_query)

    def get_all_docs_lists(self):
        from docs.models import DocList

        lists_query = Q(community_id=self.id, is_deleted=False)
        return DocList.objects.filter(lists_query).order_by("order")

    def get_last_docs(self):
        from docs.models import Doc

        docs_query = Q(list__in=self.get_docs_lists())
        return Doc.objects.filter(docs_query, is_deleted=False).exclude(type=Doc.PRIVATE)[0:5]

    def is_docs_list_exists(self):
        from docs.models import DocList

        lists_query = Q(type=DocList.LIST, is_public=True, is_deleted=False)
        lists_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        return DocList.objects.filter(lists_query).exists()

    def get_docs_lists(self):
        from docs.models import DocList

        lists_query = Q(type=DocList.LIST, is_public=True, is_deleted=False)
        lists_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        return DocList.objects.filter(lists_query).order_by("order")

    def get_admin_docs_lists(self):
        from docs.models import DocList

        lists_query = Q(type=DocList.LIST, is_deleted=False)
        lists_query.add(Q(Q(community_id=self.id)|Q(communities__id=self.pk)), Q.AND)
        return DocList.objects.filter(lists_query).order_by("order")

    def get_docs_count(self):
        from docs.models import DocList
        lists, count = DocList.objects.filter(community_id=self.id), 0
        for i in lists:
            count += i.count_docs()
        return count

    def get_last_video(self):
        from video.models import Video, VideoAlbum
        try:
            list = VideoAlbum.objects.get(community_id=self.pk, type=SoundList.MAIN)
            video_query = Q(album=list, is_deleted=False, is_public=True)
            return Video.objects.filter(video_query).order_by("-created")[0:2]
        except:
            return None

    def is_video_album_exists(self):
        return self.video_album_community.filter(community_id=self.id, type="AL", is_public=True).exists()
    def is_admin_video_album_exists(self):
        return self.video_album_community.filter(community_id=self.id, type="AL").exists()
    def get_video_albums(self):
        from video.models import VideoAlbum

        lists_query = Q(community_id=self.id, type=VideoAlbum.ALBUM, is_deleted=False, is_public=True)
        return VideoAlbum.objects.filter(lists_query).order_by("order")
    def get_admin_video_albums(self):
        from video.models import VideoAlbum

        lists_query = Q(community_id=self.id, type=VideoAlbum.ALBUM, is_deleted=False)
        return VideoAlbum.objects.filter(lists_query).order_by("order")

    def get_video_count(self):
        from video.models import VideoAlbum
        albums, count = VideoAlbum.objects.filter(community_id=self.id), 0
        for i in albums:
            count += i.count_video()
        return count

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
        trending_communities_query = ~Q(perm=Community.DELETED)
        if category_name:
            trending_communities_query.add(Q(categories__name=category_name), Q.AND)
        return trending_communities_query


    @classmethod
    def get_members(cls, community_pk):
        from users.models import User

        community_members_query = Q(communities_memberships__community__pk=community_pk)
        return User.objects.filter(community_members_query)

    @classmethod
    def get_administrators(cls, community_pk):
        from users.models import User

        community_administrators_query = Q(communities_memberships__community__pk=community_pk, communities_memberships__is_administrator=True)
        return User.objects.filter(community_administrators_query)

    @classmethod
    def get_moderators(cls, community_pk):
        from users.models import User

        community_administrators_query = Q(communities_memberships__community__pk=community_pk, communities_memberships__is_moderator=True)
        return User.objects.filter(community_administrators_query)

    @classmethod
    def get_editors(cls, community_pk):
        from users.models import User

        community_moderators_query = Q(communities_memberships__community__pk=community_pk, communities_memberships__is_editor=True)
        return User.objects.filter(community_moderators_query)

    @classmethod
    def get_advertisers(cls, community_pk):
        from users.models import User

        community_moderators_query = Q(communities_memberships__community__pk=community_pk, communities_memberships__is_advertiser=True)
        return User.objects.filter(community_moderators_query)

    @classmethod
    def get_community_follows(cls, community_pk):
        from users.models import User

        community_moderators_query = Q(communities_memberships__community__pk=community_pk, communities_memberships__is_moderator=True)
        return User.objects.filter(community_moderators_query)

    @classmethod
    def get_community_banned_users(cls, community_pk):
        community = Community.objects.get(pk=community_pk)
        community_members_query = Q()
        return community.banned_users.filter(community_members_query)

    @classmethod
    def search_community_members(cls, community_pk, query):
        from users.models import User

        db_query = Q(communities_memberships__community__pk=community_pk)
        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)
        db_query.add(community_members_query, Q.AND)
        return User.objects.filter(db_query)

    @classmethod
    def search_community_moderators(cls, community_pk, query):
        from users.models import User

        db_query = Q(communities_memberships__community__pk=community_pk, communities_memberships__is_moderator=True)
        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)
        db_query.add(community_members_query, Q.AND)
        return User.objects.filter(db_query)

    @classmethod
    def search_community_administrators(cls, community_pk, query):
        from users.models import User

        db_query = Q(communities_memberships__community__pk=community_pk, communities_memberships__is_administrator=True)
        community_members_query = Q(communities_memberships__user__username__icontains=query)
        community_members_query.add(Q(communities_memberships__user__profile__name__icontains=query), Q.OR)
        db_query.add(community_members_query, Q.AND)
        return User.objects.filter(db_query)

    @classmethod
    def search_community_banned_users(cls, community_pk, query):
        community = Community.objects.get(pk=community_pk)
        community_banned_users_query = Q(username__icontains=query)
        community_banned_users_query.add(Q(profile__name__icontains=query), Q.OR)
        return community.banned_users.filter(community_banned_users_query)

    def get_staff_members(self):
        from users.models import User

        staff_members_query = Q(communities_memberships__community_id=self.pk)
        staff_members_query.add(Q(communities_memberships__is_administrator=True) | Q(communities_memberships__is_moderator=True) | Q(communities_memberships__is_editor=True), Q.AND)
        return User.objects.filter(staff_members_query)

    def get_staff_members_ids(self):
        staff_members = self.get_staff_members().values("pk")
        return [i['pk'] for i in staff_members]

    def get_member_for_notify_ids(self):
        from notify.models import CommunityProfileNotify
        recipients = CommunityProfileNotify.objects.filter(community=self.pk).values("user")
        return [i['user'] for i in recipients] + self.get_staff_members_ids()

    def add_news_subscriber(self, user_id):
        from notify.models import CommunityNewsNotify
        if not CommunityNewsNotify.objects.filter(community=self.pk, user=user_id).exists():
            CommunityNewsNotify.objects.create(community=self.pk, user=user_id)
    def delete_news_subscriber(self, user_id):
        from notify.models import CommunityNewsNotify
        if CommunityNewsNotify.objects.filter(community=self.pk, user=user_id).exists():
            notify = CommunityNewsNotify.objects.get(community=self.pk, user=user_id)
            notify.delete()

    def add_notify_subscriber(self, user_id):
        from notify.models import CommunityProfileNotify
        if not CommunityProfileNotify.objects.filter(community=self.pk, user=user_id).exists():
            CommunityProfileNotify.objects.create(community=self.pk, user=user_id)
    def delete_notify_subscriber(self, user_id):
        from notify.models import CommunityProfileNotify
        if CommunityProfileNotify.objects.filter(community=self.pk, user=user_id).exists():
            notify = CommunityProfileNotify.objects.get(community=self.pk, user=user_id)
            notify.delete()

    def is_private(self):
        return self.type is self.COMMUNITY_TYPE_PRIVATE

    def is_closed(self):
        return self.type is self.COMMUNITY_TYPE_CLOSED

    def is_public(self):
        return self.type is self.COMMUNITY_TYPE_PUBLIC

    def is_community_playlist(self):
        from music.models import UserTempSoundList
        try:
            return UserTempSoundList.objects.get(tag=None, community=self, genre=None)
        except:
            return False

    def is_wall_close(self):
        return try_except(self.community_private_post.wall == "SP")
    def is_staff_post_member_can(self):
        return try_except(self.community_private_post.wall == "SPMC")
    def is_staff_post_all_can(self):
        return try_except(self.community_private_post.wall == "SPAC")
    def is_member_post(self):
        return try_except(self.community_private_post.wall == "MP")
    def is_member_post_all_can(self):
        return try_except(self.community_private_post.wall == "MPAC")
    def is_all_can_post(self):
        return try_except(self.community_private_post.wall == "AC")
    def is_comment_post_send_admin(self):
        return try_except(self.community_private_post.comment == "CA")
    def is_comment_post_send_member(self):
        return try_except(self.community_private_post.comment == "CM")
    def is_comment_post_send_all(self):
        return try_except(self.community_private_post.comment == "CNM")

    def is_photo_upload_admin(self):
        return try_except(self.community_private_photo.photo == "PA")
    def is_photo_upload_member(self):
        return try_except(self.community_private_photo.photo == "PM")
    def is_photo_upload_nomember(self):
        return try_except(self.community_private_photo.photo == "PNM")
    def is_comment_photo_send_admin(self):
        return try_except(self.community_private_photo.comment == "CA")
    def is_comment_photo_send_member(self):
        return try_except(self.community_private_photo.comment == "CM")
    def is_comment_photo_send_all(self):
        return try_except(self.community_private_photo.comment == "CNM")

    def is_good_upload_admin(self):
        return try_except(self.community_private_good.good == "GA")
    def is_good_upload_member(self):
        return try_except(self.community_private_good.good == "GM")
    def is_good_upload_nomember(self):
        return try_except(self.community_private_good.good == "GNM")
    def is_comment_good_send_admin(self):
        return try_except(self.community_private_good.comment == "CA")
    def is_comment_good_send_member(self):
        return try_except(self.community_private_good.comment == "CM")
    def is_comment_good_send_all(self):
        return try_except(self.community_private_good.comment == "CNM")

    def is_video_upload_admin(self):
        return try_except(self.community_private_video.video == "VA")
    def is_video_upload_member(self):
        return try_except(self.community_private_video.video == "VM")
    def is_video_upload_nomember(self):
        return try_except(self.community_private_video.video == "VNM")
    def is_comment_video_send_admin(self):
        return try_except(self.community_private_video.comment == "CA")
    def is_comment_video_send_member(self):
        return try_except(self.community_private_video.comment == "CM")
    def is_comment_video_send_all(self):
        return try_except(self.community_private_video.comment == "CNM")

    def add_administrator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = True
        user_membership.is_editor = False
        user_membership.is_advertiser = False
        self.add_notify_subscriber(user.pk)
        user_membership.save()
        return user_membership
    def add_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = True
        user_membership.is_administrator = False
        user_membership.is_editor = False
        user_membership.is_advertiser = False
        self.add_notify_subscriber(user.pk)
        user_membership.save()
        return user_membership
    def add_editor(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = False
        user_membership.is_editor = True
        user_membership.is_advertiser = False
        self.add_notify_subscriber(user.pk)
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
        self.delete_notify_subscriber(user.pk)
        return user_membership
    def remove_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.save(update_fields=['is_moderator'])
        self.delete_notify_subscriber(user.pk)
        return user_membership
    def remove_editor(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_editor = False
        user_membership.save(update_fields=['is_editor'])
        self.delete_notify_subscriber(user.pk)
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
        self.delete_news_subscriber(user.pk)
        user_membership.delete()

    def create_invite(self, creator, invited_user):
        from invitations.models import CommunityInvite

        CommunityInvite = get_community_invite_model()
        return CommunityInvite.create_community_invite(creator=creator, invited_user=invited_user, community=self)

    def count_members(self):
        return self.memberships.values("pk").count()

    def count_members_ru(self):
        count = self.memberships.values("pk").count()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " подписчик"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " подписчика"
        else:
            return str(count) + " подписчиков"

    def get_community_notify(self):
        from notify.models import Notify
        query = Q(community_id=self.pk, status="U")|Q(community_id=self.pk, community__isnull=True, user_set__isnull=True, status="R")
        return Notify.objects.only('created').filter(query)

    def count_community_unread_notify(self, user_pk):
        from notify.models import Notify

        query = Q(community_id=self.pk, recipient_id=user_pk, status="U")
        return Notify.objects.filter(query).values("pk").count()

    def count_unread_notify(self, user_pk):
        count = self.count_community_unread_notify(user_pk)
        if count > 0:
            return '<span class="tab_badge badge-success" style="font-size: 60%;">{}</span>'.format(str(count))
        else:
            return ''

    def read_community_notify(self, user_pk):
        from notify.models import Notify

        Notify.c_notify_unread(self.pk, user_pk)


    ''''' модерация '''''
    def get_longest_community_penalties(self):
        return self.community_penalties.filter(community=self)[0].expiration
    def get_moderated_description(self):
        return self.moderated_community.filter(community=self)[0].description
    def is_suspended(self):
        from django.utils import timezone
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
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_membership(cls, user, community, is_administrator=False, is_editor=False, is_advertiser=False, is_moderator=False):
        community.add_news_subscriber(user.pk)
        return cls.objects.create(user=user, community=community, is_administrator=is_administrator, is_editor=is_editor, is_advertiser=is_advertiser, is_moderator=is_moderator)

    class Meta:
        #unique_together = (('user', 'community'),)
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
    #item = models.ForeignKey("posts.Post", on_delete=models.CASCADE, related_name='+', null=True, blank=True, verbose_name="Пост")
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='logs', null=False, blank=False, verbose_name="Сообщество")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создан")
    id = models.BigAutoField(primary_key=True)

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


class CommunityInvite(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='created_communities_invites', null=False,blank=False, verbose_name="Кто приглашает в сообщество")
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='communities_invites', null=False, blank=False, verbose_name="Кого приглашают в сообщество")
    community = models.ForeignKey(Community, db_index=False, on_delete=models.CASCADE, related_name='invites', null=False, blank=False, verbose_name="Сообщество")

    @classmethod
    def create_community_invite(cls, creator, invited_user, community):
        return cls.objects.create(creator=creator, invited_user=invited_user, community=community)

    @classmethod
    def is_user_with_username_invited_to_community(cls, username, community_pk):
        return cls.objects.filter(community__pk=community_pk, invited_user__username=username).exists()

    class Meta:
        #unique_together = (('invited_user', 'community', 'creator'),)
        verbose_name = 'Приглашение в сообщество'
        verbose_name_plural = 'Приглашения в сообщества'

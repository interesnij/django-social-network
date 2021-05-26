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
    PRIVATE, CLOSED, MANAGER, THIS_PROCESSING, PUBLIC = 'PRI', 'CLO', 'MAN', '_PRO', 'PUB'
    THIS_DELETED, THIS_PRIVATE_DELETED, THIS_CLOSED_DELETED, THIS_MANAGER_DELETED = '_DELO', '_DELP', '_DELC', '_DELM'
    THIS_BANNER_OPEN, THIS_BANNER_PRIVATE, THIS_BANNER_CLOSED, THIS_BANNER_MANAGER = '_BANO', '_BANP', '_BANC', '_BANM'
    THIS_SUSPENDED_OPEN, THIS_SUSPENDED_PRIVATE, THIS_SUSPENDED_CLOSED, THIS_SUSPENDED_MANAGER = '_SUSO', '_SUSP', '_SUSC', '_SUSM'
    THIS_BLOCKED_OPEN, THIS_BLOCKED_PRIVATE, THIS_BLOCKED_CLOSED, THIS_BLOCKED_MANAGER = '_BLOO', '_BLOP', '_BLOC', '_BLOM'
    TYPE = (
        (CLOSED, 'Закрытый'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PUBLIC, 'Открытый'), (THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Открытый удалённый'),(THIS_PRIVATE_DELETED, 'Приватный удалённый'),(THIS_CLOSED_DELETED, 'Закрытый удалённый'),(THIS_MANAGER_DELETED, 'Менеджерский удалённый'),
        (THIS_BANNER_OPEN, 'Открытый баннер'),(THIS_BANNER_PRIVATE, 'Приватный баннер'),(THIS_BANNER_CLOSED, 'Закрытый баннер'),(THIS_BANNER_MANAGER, 'Менеджерский баннер'),
        (THIS_SUSPENDED_OPEN, 'Открытый замороженный'),(THIS_SUSPENDED_PRIVATE, 'Приватный замороженный'), (THIS_SUSPENDED_CLOSED, 'Закрытый замороженный'),(THIS_SUSPENDED_MANAGER, 'Менеджерский замороженный'),
        (THIS_BLOCKED_OPEN, 'Открытый блокнутый'),(THIS_BLOCKED_PRIVATE, 'Приватный блокнутый'), (THIS_BLOCKED_CLOSED, 'Закрытый блокнутый'),(THIS_BLOCKED_MANAGER, 'Менеджерский блокнутый'),
    )

    CHILD, STANDART, VERIFIED_SEND, VERIFIED = 'CH', 'ST', 'VS', 'VE'
    PERM = (
        (CHILD, 'Детская'),(STANDART, 'Обычные права'),(VERIFIED_SEND, 'Запрос на проверку'),(VERIFIED, 'Провернный'),
    )

    category = models.ForeignKey(CommunitySubCategory, on_delete=models.CASCADE, related_name='+', verbose_name="Подкатегория сообщества")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_communities', null=False, blank=False, verbose_name="Создатель")
    name = models.CharField(max_length=settings.COMMUNITY_NAME_MAX_LENGTH, blank=False, null=False, verbose_name="Название" )
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    type = models.CharField(choices=TYPE, default=THIS_PROCESSING, max_length=5)
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_community_cover_directory)
    perm = models.CharField(max_length=5, choices=PERM, default=STANDART, verbose_name="Уровень доступа")
    have_link = models.CharField(max_length=17, blank=True, verbose_name='Ссылка')
    banned_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='banned_of_communities', verbose_name="Черный список")

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'сообщества'
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.name

    def plus_photos(self, count):
        self.community_info.photos += count
        return self.community_info.save(update_fields=['photos'])
    def minus_photos(self, count):
        self.community_info.photos -= count
        return self.community_info.save(update_fields=['photos'])
    def plus_goods(self, count):
        self.community_info.goods += count
        return self.community_info.save(update_fields=['goods'])
    def minus_goods(self, count):
        self.community_info.goods -= count
        return self.community_info.save(update_fields=['goods'])
    def plus_posts(self, count):
        self.community_info.posts += count
        return self.community_info.save(update_fields=['posts'])
    def minus_posts(self, count):
        self.community_info.posts -= count
        return self.community_info.save(update_fields=['posts'])
    def plus_videos(self, count):
        self.community_info.videos += count
        return self.community_info.save(update_fields=['videos'])
    def minus_videos(self, count):
        self.community_info.videos -= count
        return self.community_info.save(update_fields=['videos'])
    def plus_docs(self, count):
        self.community_info.docs += count
        return self.community_info.save(update_fields=['docs'])
    def minus_docs(self, count):
        self.community_info.docs -= count
        return self.community_info.save(update_fields=['docs'])
    def plus_tracks(self, count):
        self.community_info.tracks += count
        return self.community_info.save(update_fields=['tracks'])
    def minus_tracks(self, count):
        self.community_info.tracks -= count
        return self.community_info.save(update_fields=['tracks'])
    def plus_articles(self, count):
        self.community_info.articles += count
        return self.community_info.save(update_fields=['articles'])
    def minus_articles(self, count):
        self.community_info.articles -= count
        return self.community_info.save(update_fields=['articles'])
    def plus_member(self):
        self.community_info.members = self.community_info.members + 1
        return self.community_info.save(update_fields=['members'])
    def minus_member(self):
        self.community_info.members -= 1
        return self.community_info.save(update_fields=['members'])

    def is_deleted(self):
        return self.type == Community.THIS_DELETED
    def is_standart(self):
        return self.perm == Community.STANDART
    def is_verified_send(self):
        return self.perm == Community.VERIFIED_SEND
    def is_verified(self):
        return self.perm == Community.VERIFIED
    def is_child(self):
        return self.perm == Community.CHILD
    def is_suspended(self):
        return self.type[:4] == "_SUS"
    def is_closed(self):
        return self.type[:4] == "_BLO"
    def is_have_warning_banner(self):
        return self.type[:4] == "_BAN"
    def is_private(self):
        return self.type == self.PRIVATE
    def is_close(self):
        return self.type == self.CLOSED
    def is_public(self):
        return self.type == self.PUBLIC
    def is_open(self):
        return self.type[0] != "_"

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
        return [i['id'] for i in Post.objects.filter(list__in=self.get_admin_all_post_lists()).values('id')]

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
    def create_community(cls, name, category, creator, type):
        community = cls.objects.create(name=name, creator=creator, type=type, category=category)
        CommunityMembership.create_membership(user=creator, is_administrator=True, community=community)
        community.save()
        creator.create_or_plus_populate_community(community.pk)
        community.add_news_subscriber(creator.pk)
        community.add_notify_subscriber(creator.pk)
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
        return cls.objects.filter(pk=community_pk, type='_CLO').exists()

    @classmethod
    def get_community_for_user_with_id(cls, community_pk, user_id):
        query = Q(pk=community_pk)
        query.add(~Q(banned_users__id=user_id, type__contains="_"), Q.AND)
        return cls.objects.get(query)

    @classmethod
    def count_user_community(cls, user_pk):
        query = Q(memberships__user_id=user_id)
        query.add(~Q(type__contains='_'), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def search_communities_with_query(cls, query):
        query = cls._make_search_communities_query(query=query)
        return cls.objects.filter(query)

    @classmethod
    def _make_search_communities_query(cls, query):
        communities_query = Q(name__icontains=query)
        communities_query.add(Q(title__icontains=query), Q.OR)
        communities_query.add(~Q(type__contains="_"), Q.AND)
        return communities_query

    @classmethod
    def get_trending_communities_for_user_with_id(cls, user_id, category_name=None):
        trending_communities_query = cls._make_trending_communities_query(category_name=category_name)
        trending_communities_query.add(~Q(banned_users__id=user_id), Q.AND)
        return cls._get_trending_communities_with_query(query=trending_communities_query)

    def get_fix_list(self):
        from posts.models import PostList
        return PostList.objects.get(community_id=self.pk, type=PostList.THIS_FIXED)

    def get_draft_posts(self):
        from posts.models import PostList
        list = PostList.objects.get(community_id=self.pk, type="_DRA")
        return list.get_items()
    def get_count_draft_posts(self):
        from posts.models import PostList
        list = PostList.objects.get(community_id=self.pk, type="_DRA")
        return list.count_items()

    def get_count_articles(self):
        return self.community_info.articles

    def id_draft_posts_exists(self):
        return self.get_count_draft_posts() > 0

    def get_draft_posts_for_user(self, user_pk):
        from posts.models import PostList
        list = PostList.objects.get(community_id=self.pk, type="_DRA")
        posts_query = list.get_items()
        return list.get_items().filter(creator_id=user_pk)
    def get_count_draft_posts_for_user(self, user_pk):
        from posts.models import PostList
        list = PostList.objects.get(community_id=self.pk, type="_DRA")
        posts_query = list.get_items()
        return list.get_items().filter(creator_id=user_pk).values("pk").count()

    def get_count_photos(self):
        return self.community_info.photos

    def get_profile_photos(self):
        return self.get_photo_list().get_items()[:6]

    def get_goods_count(self):
        return self.community_info.goods

    def get_good_list(self):
        from goods.models import GoodList
        return GoodList.objects.get(community_id=self.pk, type=GoodList.MAIN)
    def get_post_list(self):
        from posts.models import PostList
        return PostList.objects.get(community_id=self.pk, type=PostList.MAIN)
    def get_playlist(self):
        from music.models import SoundList
        return SoundList.objects.get(community_id=self.pk, type=SoundList.MAIN)
    def get_video_list(self):
        from video.models import VideoList
        return VideoList.objects.get(community_id=self.pk, type=VideoList.MAIN)
    def get_photo_list(self):
        from gallery.models import PhotoList
        return PhotoList.objects.get(community_id=self.pk, type=PhotoList.MAIN)
    def get_doc_list(self):
        from docs.models import DocList
        return DocList.objects.get(community_id=self.pk, type=DocList.MAIN)

    def get_post_lists(self):
        from posts.models import PostList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return PostList.objects.filter(query)

    def get_survey_lists(self):
        from survey.models import SurveyList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return SurveyList.objects.filter(query)

    def get_photo_lists(self):
        from gallery.models import PhotoList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return PhotoList.objects.filter(query)

    def get_video_lists(self):
        from video.models import VideoList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return VideoList.objects.filter(query)

    def get_playlists(self):
        from music.models import SoundList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return SoundList.objects.filter(query)

    def get_good_lists(self):
        from goods.models import GoodList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return GoodList.objects.filter(query)

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
        from communities.model.settings import CommunityInfo

        info = CommunityInfo.objects.get(community=self)
        info.b_avatar = photo_input
        info.save(update_fields=['b_avatar'])
        new_img = get_thumbnailer(info.b_avatar)['avatar'].url.replace('media/', '')
        info.b_avatar = new_img
        info.save(update_fields=['b_avatar'])
        return info.b_avatar

    def get_b_avatar(self):
        try:
            return self.community_info.b_avatar.url
        except:
            return None

    def get_avatar(self):
        try:
            return self.s_avatar.url
        except:
            return None

    def get_music_count(self):
        return self.community_info.tracks
    def get_docs_count(self):
        return self.community_info.docs
    def get_photos_count(self):
        return self.community_info.photos
    def get_videos_count(self):
        return self.community_info.videos
    def get_posts_count(self):
        return self.community_info.posts

    def get_last_music(self):
        return self.get_playlist().get_items()[0:5]

    def get_last_docs(self):
        return self.get_doc_list().get_items()[0:5]

    def get_last_video(self):
        return self.get_video_list().get_items()[0:2]

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
        trending_communities_query = ~Q(type__contains="_")
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

    def is_community_playlist(self):
        from music.models import UserTempSoundList
        return UserTempSoundList.objects.filter(tag=None, community=self, genre=None).exists()

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

    def is_can_fixed_post(self):
        from posts.models import PostList
        try:
            list = PostList.objects.get(community_id=self.pk, type=PostList.THIS_FIXED)
            return list.count_fix_items() < 10
        except:
            return None

    def add_administrator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = True
        user_membership.is_editor = False
        user_membership.is_advertiser = False
        self.add_notify_subscriber(user.pk)
        user_membership.save()
    def add_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = True
        user_membership.is_administrator = False
        user_membership.is_editor = False
        user_membership.is_advertiser = False
        self.add_notify_subscriber(user.pk)
        user_membership.save()
    def add_editor(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = False
        user_membership.is_editor = True
        user_membership.is_advertiser = False
        self.add_notify_subscriber(user.pk)
        user_membership.save()
    def add_advertiser(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.is_administrator = False
        user_membership.is_editor = False
        user_membership.is_advertiser = True
        user_membership.save()

    def remove_administrator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_administrator = False
        user_membership.save(update_fields=['is_administrator'])
        self.delete_notify_subscriber(user.pk)
    def remove_moderator(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_moderator = False
        user_membership.save(update_fields=['is_moderator'])
        self.delete_notify_subscriber(user.pk)
    def remove_editor(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_editor = False
        user_membership.save(update_fields=['is_editor'])
        self.delete_notify_subscriber(user.pk)
    def remove_advertiser(self, user):
        user_membership = self.memberships.get(user=user)
        user_membership.is_advertiser = False
        user_membership.save(update_fields=['is_advertiser'])

    def add_member(self, user):
        CommunityMembership.create_membership(user=user, community=self)
        user.create_or_plus_populate_community(self.pk)
        self.add_news_subscriber(user.pk)
    def remove_member(self, user):
        user_membership = self.memberships.get(user=user).delete()
        self.minus_member()
        user.minus_communities(1)
        user.delete_populate_community(self.pk)
        self.delete_news_subscriber(user.pk)

    def count_members(self):
        from communities.model.settings import CommunityInfo
        profile = CommunityInfo.objects.get(community=self)
        return profile.members

    def count_members_ru(self):
        count = self.count_members()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " подписчик"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " подписчика"
        else:
            return str(count) + " подписчиков"

    def get_community_notify(self):
        from notify.models import Notify
        query = Q(community_id=self.pk)
        query.add(Q(Q(status="U")|Q(community__isnull=True, user_set__isnull=True, status="R")), Q.AND)
        return Notify.objects.only('created').filter(query)

    def count_community_unread_notify(self, user_pk):
        from notify.models import Notify
        return Notify.objects.filter(community_id=self.pk, recipient_id=user_pk, status="U").values("pk").count()

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
        from managers.models import Moderated
        return Moderated.objects.filter(object_id=self.pk, type="COM")[0].description

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
        community.plus_member()
        user.plus_communities(1)
        return cls.objects.create(user=user, community=community, is_administrator=is_administrator, is_editor=is_editor, is_advertiser=is_advertiser, is_moderator=is_moderator)

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

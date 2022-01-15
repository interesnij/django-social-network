import uuid
from django.conf import settings
from django.db import models
from django.db.models import Q
from pilkit.processors import ResizeToFill, ResizeToFit
from communities.helpers import upload_to_community_avatar_directory, upload_to_community_cover_directory
from imagekit.models import ProcessedImageField
from common.utils import try_except
from django.contrib.postgres.indexes import BrinIndex
from users.models import User


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
    PRIVATE, CLOSED, MANAGER, PUBLIC = 'PRI','CLO','MAN','PUB'
    DELETED, PRIVATE_DELETED, CLOSED_DELETED, MANAGER_DELETED = '_DELO', '_DELP', '_DELC', '_DELM'
    BANNER_OPEN, BANNER_PRIVATE, BANNER_CLOSED, BANNER_MANAGER = '_BANO', '_BANP', '_BANC', '_BANM'
    SUSPENDED_OPEN, SUSPENDED_PRIVATE, SUSPENDED_CLOSED, SUSPENDED_MANAGER = '_SUSO', '_SUSP', '_SUSC', '_SUSM'
    BLOCKED_OPEN, BLOCKED_PRIVATE, BLOCKED_CLOSED, BLOCKED_MANAGER = '_BLOO', '_BLOP', '_BLOC', '_BLOM'
    TYPE = (
        (CLOSED, 'Закрытый'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(PUBLIC, 'Открытый'),
        (DELETED, 'Открытый удалённый'),(PRIVATE_DELETED, 'Приватный удалённый'),(CLOSED_DELETED, 'Закрытый удалённый'),(MANAGER_DELETED, 'Менеджерский удалённый'),
        (BANNER_OPEN, 'Открытый баннер'),(BANNER_PRIVATE, 'Приватный баннер'),(BANNER_CLOSED, 'Закрытый баннер'),(BANNER_MANAGER, 'Менеджерский баннер'),
        (SUSPENDED_OPEN, 'Открытый замороженный'),(SUSPENDED_PRIVATE, 'Приватный замороженный'), (SUSPENDED_CLOSED, 'Закрытый замороженный'),(SUSPENDED_MANAGER, 'Менеджерский замороженный'),
        (BLOCKED_OPEN, 'Открытый блокнутый'),(BLOCKED_PRIVATE, 'Приватный блокнутый'), (BLOCKED_CLOSED, 'Закрытый блокнутый'),(BLOCKED_MANAGER, 'Менеджерский блокнутый'),
    )

    CHILD, STANDART, VERIFIED_SEND, VERIFIED = 'CH', 'ST', 'VS', 'VE'
    PERM = (
        (CHILD, 'Детская'),(STANDART, 'Обычные права'),(VERIFIED_SEND, 'Запрос на проверку'),(VERIFIED, 'Провернный'),
    )

    category = models.ForeignKey(CommunitySubCategory, on_delete=models.CASCADE, related_name='+', verbose_name="Подкатегория сообщества")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_communities', null=False, blank=False, verbose_name="Создатель")
    name = models.CharField(max_length=settings.COMMUNITY_NAME_MAX_LENGTH, blank=False, null=False, verbose_name="Название" )
    description = models.TextField(max_length=settings.COMMUNITY_DESCRIPTION_MAX_LENGTH, blank=True, null=True, verbose_name="Описание" )
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    status = models.CharField(max_length=100, blank=True, verbose_name="статус-слоган")
    type = models.CharField(choices=TYPE, max_length=5)
    perm = models.CharField(max_length=5, choices=PERM, default=STANDART, verbose_name="Уровень доступа")
    have_link = models.CharField(max_length=17, blank=True, verbose_name='Ссылка')
    s_avatar = models.ImageField(blank=True, upload_to=upload_to_community_avatar_directory)
    b_avatar = models.ImageField(blank=True, upload_to=upload_to_community_avatar_directory)
    cover = ProcessedImageField(blank=True, format='JPEG',options={'quality': 100},upload_to=upload_to_community_cover_directory,processors=[ResizeToFit(width=1024, upscale=False)])

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'сообщества'
        indexes = (BrinIndex(fields=['created']),)

    def __str__(self):
        return self.name

    def get_b_avatar(self):
        if self.get_avatar_pk():
            return '<img src="' + self.b_avatar.url + '" class="detail_photo pointer" photo-pk="' + str(self.get_avatar_pk()) + '">'
        else:
            return '/static/images/no_img/list.jpg'

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
        return self.type == Community.DELETED
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
            return '<img style="border-radius:50px;width:50px;" alt="image" src="' + self.s_avatar.url + '" />'
        else:
            return '<svg fill="currentColor" class="svg_default svg_default_50" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"></path></svg>'

    def get_s_avatar(self):
        if self.s_avatar:
            return '<img style="border-radius:30px;width:30px;" alt="image" src="' + self.s_avatar.url + '" />'
        else:
            return '<svg fill="currentColor" class="svg_default svg_default_30" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"></path><path d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"></path></svg>'

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

    @classmethod
    def create_community(cls, name, category, creator, type):
        community = cls.objects.create(name=name, creator=creator, type=type, category=category)
        CommunityMembership.create_membership(user=creator, is_administrator=True, community=community)
        community.save()
        creator.plus_community_visited(community.pk)
        community.add_news_subscriber_in_main_list(creator.pk)
        community.add_notify_subscriber_in_main_list(creator.pk)
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

    def get_draft_posts(self):
        from posts.models import PostsList
        list = PostsList.objects.get(community_id=self.pk, type="_DRA")
        return list.get_items()
    def get_count_draft_posts(self):
        from posts.models import PostsList
        list = PostsList.objects.get(community_id=self.pk, type="_DRA")
        return list.count_items()

    def get_count_articles(self):
        return self.community_info.articles

    def id_draft_posts_exists(self):
        return self.get_count_draft_posts() > 0

    def get_draft_posts_for_user(self, user_pk):
        from posts.models import PostsList
        list = PostsList.objects.get(community_id=self.pk, type="_DRA")
        posts_query = list.get_items()
        return list.get_items().filter(creator_id=user_pk)
    def get_count_draft_posts_for_user(self, user_pk):
        from posts.models import PostsList
        list = PostsList.objects.get(community_id=self.pk, type="_DRA")
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
        from posts.models import PostsList
        return PostsList.objects.get(community_id=self.pk, type=PostsList.MAIN)
    def get_playlist(self):
        from music.models import MusicList
        return MusicList.objects.get(community_id=self.pk, type=MusicList.MAIN)
    def get_video_list(self):
        from video.models import VideoList
        return VideoList.objects.get(community_id=self.pk, type=VideoList.MAIN)
    def get_photo_list(self):
        from gallery.models import PhotoList
        return PhotoList.objects.get(community_id=self.pk, type=PhotoList.MAIN)
    def get_avatar_pk(self):
        try:
            from gallery.models import PhotoList
            list = PhotoList.objects.get(community_id=self.pk, type=PhotoList.AVATAR)
            return list.get_items().first().pk
        except:
            return None
    def get_doc_list(self):
        from docs.models import DocsList
        return DocsList.objects.get(community_id=self.pk, type=DocsList.MAIN)

    def get_post_lists(self):
        from posts.models import PostsList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return PostsList.objects.filter(query)
    def get_selected_post_list_pk(self):
        from communities.model.list import CommunityPostsListPosition
        list = CommunityPostsListPosition.objects.filter(community=self.pk, type=1).first()
        return list.list

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

    def get_doc_lists(self):
        from docs.models import DocsList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return DocsList.objects.filter(query)

    def get_video_lists(self):
        from video.models import VideoList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return VideoList.objects.filter(query)

    def get_playlists(self):
        from music.models import MusicList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return MusicList.objects.filter(query)

    def get_good_lists(self):
        from goods.models import GoodList
        query = Q(community_id=self.id)
        query.add(~Q(type__contains="_"), Q.AND)
        return GoodList.objects.filter(query)

    def get_6_photos(self):
        from gallery.models import Photo
        return Photo.objects.filter(community_id=self.pk, type="PUB")[:6]
    def get_6_docs(self):
        from docs.models import Doc
        return Doc.objects.filter(community_id=self.pk, type="PUB")[:6]
    def get_6_tracks(self):
        from music.models import Music
        return Music.objects.filter(community_id=self.pk, type="PUB")[:6]
    def get_2_videos(self):
        from video.models import Video
        return Video.objects.filter(community_id=self.pk, type="PUB")[:2]
    def get_3_goods(self):
        from goods.models import Good
        return Good.objects.filter(community_id=self.pk, type="PUB")[:3]

    def is_anon_user_can_see_post(self):
        private = self.community_private2
        return private.can_see_post == 1
    def is_anon_user_can_see_photo(self):
        private = self.community_private2
        return private.can_see_photo == 1
    def is_anon_user_can_see_member(self):
        private = self.community_private2
        return private.can_see_member == 1
    def is_anon_user_can_see_doc(self):
        private = self.community_private2
        return private.can_see_doc == 1
    def is_anon_user_can_see_music(self):
        private = self.community_private2
        return private.can_see_music == 1
    def is_anon_user_can_see_video(self):
        private = self.community_private2
        return private.can_see_video == 1
    def is_anon_user_can_see_good(self):
        private = self.community_private2
        return private.can_see_good == 1
    def is_anon_user_can_see_stat(self):
        private = self.community_private2
        return private.can_see_stat == 1

    def is_user_can_see_photo(self, user_id):
        private = self.community_private2
        if private.can_see_photo == 1:
            return True
        elif private.can_see_photo == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_photo == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_photo == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_photo == 5:
            return not user_pk in self.get_can_see_photo_exclude_users_ids()
        elif private.can_see_photo == 6:
            return user_pk in self.get_can_see_photo_include_users_ids()
        return False
    def is_user_can_see_stat(self, user_id):
        private = self.community_private2
        if private.can_see_stat == 1:
            return True
        elif private.can_see_stat == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_stat == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_stat == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_stat == 5:
            return not user_pk in self.get_can_see_stat_exclude_users_ids()
        elif private.can_see_stat == 6:
            return user_pk in self.get_can_see_stat_include_users_ids()
        return False
    def is_user_can_see_settings(self, user_id):
        private = self.community_private2
        if private.can_see_settings == 1:
            return True
        elif private.can_see_settings == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_settings == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_settings == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_settings == 5:
            return not user_pk in self.get_can_see_settings_exclude_users_ids()
        elif private.can_see_settings == 6:
            return user_pk in self.get_can_see_settings_include_users_ids()
        return False

    def is_user_can_see_post(self, user_id):
        private = self.community_private2
        if private.can_see_post == 1:
            return True
        elif private.can_see_post == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_post == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_post == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_post == 5:
            return not user_pk in self.get_can_see_post_exclude_users_ids()
        elif private.can_see_post == 6:
            return user_pk in self.get_can_see_post_include_users_ids()
        return False

    def is_user_can_send_message(self, user_id):
        private = self.community_private2
        if private.can_send_message == 1:
            return True
        elif private.can_send_message == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_send_message == 3 and user_id == self.creator.pk:
            return True
        elif private.can_send_message == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_send_message == 5:
            return not user_pk in self.get_can_send_message_exclude_users_ids()
        elif private.can_send_message == 6:
            return user_pk in self.get_can_send_message_include_users_ids()
        return False

    def is_user_can_see_good(self, user_id):
        private = self.community_private2
        if private.can_see_good == 1:
            return True
        elif private.can_see_good == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_good == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_good == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_good == 5:
            return not user_pk in self.get_can_see_good_exclude_users_ids()
        elif private.can_see_good == 6:
            return user_pk in self.get_can_see_good_include_users_ids()
        return False

    def is_user_can_see_video(self, user_id):
        private = self.community_private2
        if private.can_see_video == 1:
            return True
        elif private.can_see_video == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_video == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_video == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_video == 5:
            return not user_pk in self.get_can_see_video_exclude_users_ids()
        elif private.can_see_video == 6:
            return user_pk in self.get_can_see_video_include_users_ids()
        return False

    def is_user_can_see_music(self, user_id):
        private = self.community_private2
        if private.can_see_music == 1:
            return True
        elif private.can_see_music == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_music == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_music == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_music == 5:
            return not user_pk in self.get_can_see_music_exclude_users_ids()
        elif private.can_see_music == 6:
            return user_pk in self.get_can_see_music_include_users_ids()
        return False

    def is_user_can_see_doc(self, user_id):
        private = self.community_private2
        if private.can_see_doc == 1:
            return True
        elif private.can_see_doc == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_doc == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_doc == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_doc == 5:
            return not user_pk in self.get_can_see_doc_exclude_users_ids()
        elif private.can_see_doc == 6:
            return user_pk in self.get_can_see_doc_include_users_ids()
        return False

    def is_user_can_see_member(self, user_id):
        private = self.community_private2
        if private.can_see_member == 1:
            return True
        elif private.can_see_member == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_member == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_member == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_member == 5:
            return not user_pk in self.get_can_see_member_exclude_users_ids()
        elif private.can_see_member == 6:
            return user_pk in self.get_can_see_member_include_users_ids()
        return False
    def is_user_can_see_log(self, user_id):
        private = self.community_private2
        if private.can_see_log == 1:
            return True
        elif private.can_see_log == 2 and user_id in self.get_members_ids():
            return True
        elif private.can_see_log == 3 and user_id == self.creator.pk:
            return True
        elif private.can_see_log == 4 and user_id in self.get_staff_members_ids():
            return True
        elif private.can_see_log == 5:
            return not user_pk in self.get_can_see_log_exclude_users_ids()
        elif private.can_see_log == 6:
            return user_pk in self.get_can_see_log_include_users_ids()
        return False

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
        return User.objects.filter(communities_memberships__community__pk=community_pk)

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

    def get_members_ids(self):
        return [i['user_id'] for i in CommunityMembership.objects.filter(community_id=self.pk).values("user_id")]

    def get_staff_members_ids(self):
        staff_members = self.get_staff_members().values("pk")
        return [i['pk'] for i in staff_members]

    def get_member_for_notify_ids(self):
        from notify.models import CommunityProfileNotify
        recipients = CommunityProfileNotify.objects.filter(community=self.pk).values("user")
        return [i['user'] for i in recipients] + self.get_staff_members_ids()

    def add_news_subscriber_in_main_list(self, user_id):
        from users.model.list import ListUC, NewsUC
        list = ListUC.objects.get(owner=user_id, type=1)
        if not NewsUC.objects.filter(list=list, owner=user_id, community=self.pk).exists():
            NewsUC.objects.create(list=list, owner=user_id, community=self.pk)
    def delete_news_subscriber_from_main_list(self, user_id):
        from users.model.list import ListUC, NewsUC
        list = ListUC.objects.get(owner=user_id, type=1)
        if NewsUC.objects.filter(list=list, owner=user_id, community=self.pk).exists():
            notify = NewsUC.objects.get(list=list, owner=user_id, community=self.pk)
            notify.delete()
    def add_news_subscriber_in_list(self, user_id, list_id):
        from users.model.list import ListUC, NewsUC
        if not NewsUC.objects.filter(list_id=list_id, owner=user_id, community=self.pk).exists():
            NewsUC.objects.create(list_id=list_id, owner=user_id, community=self.pk)
    def delete_news_subscriber_from_list(self, user_id, list_id):
        from users.model.list import ListUC, NewsUC
        if NewsUC.objects.filter(list_id=list_id, owner=user_id, community=self.pk).exists():
            notify = NewsUC.objects.get(list_id=list_id, owner=user_id, community=self.pk)
            notify.delete()

    def add_notify_subscriber_in_main_list(self, user_id):
        from users.model.list import ListUC, NotifyUC
        list = ListUC.objects.get(owner=user_id, type=1)
        if not NotifyUC.objects.filter(list=list, owner=user_id, community=self.pk).exists():
            NotifyUC.objects.create(list=list, owner=user_id, community=self.pk)
    def delete_notify_subscriber_from_main_list(self, user_id):
        from users.model.list import ListUC, NotifyUC
        list = ListUC.objects.get(owner=user_id, type=1)
        if NotifyUC.objects.filter(list=list, owner=user_id, community=self.pk).exists():
            notify = NotifyUC.objects.get(list=list, owner=user_id, community=self.pk)
            notify.delete()
    def add_notify_subscriber_in_list(self, user_id, list_id):
        from users.model.list import ListUC, NotifyUC
        if not NotifyUC.objects.filter(list_id=list_id, owner=user_id, community=self.pk).exists():
            NotifyUC.objects.create(list_id=list_id, owner=user_id, community=self.pk)
    def delete_notify_subscriber_from_list(self, user_id, list_id):
        from users.model.list import ListUC, NotifyUC
        if NotifyUC.objects.filter(list_id=list_id, owner=user_id, community=self.pk).exists():
            notify = NotifyUC.objects.get(list_id=list_id, owner=user_id, community=self.pk)
            notify.delete()

    def is_community_playlist(self):
        from music.models import UserTempMusicList
        return UserTempMusicList.objects.filter(community=self, genre=None).exists()

    def get_fixed_posts(self):
        from posts.models import Post
        return Post.objects.filter(community_id=self.pk, type=Post.FIXED)
    def get_fixed_posts_ids(self):
        from posts.models import Post
        list = Post.objects.filter(community_id=self.pk, type=Post.FIXED).values("pk")
        return [i['pk'] for i in list]

    def count_fixed_posts(self):
        from posts.models import Post
        return Post.objects.filter(community_id=self.pk, type=Post.FIXED).values("pk").count()

    def is_can_fixed_post(self):
        return self.count_fixed_posts() < 10

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
        user.plus_community_visited(self.pk)
        self.add_news_subscriber_in_main_list(user.pk)
    def remove_member(self, user):
        user_membership = self.memberships.get(user=user).delete()
        self.minus_member()
        user.minus_communities(1)
        self.delete_news_subscriber_from_list(user.pk)

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

    def get_can_see_community_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_community=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_community_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_community=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_community_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_community_exclude_users_ids())
    def get_can_see_community_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_community_include_users_ids())

    def get_can_see_info_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_info=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_info_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_info=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_info_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_info_exclude_users_ids())
    def get_can_see_info_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_info_include_users_ids())

    def get_can_see_member_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_member=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_member_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_member=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_member_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_member_exclude_users_ids())
    def get_can_see_member_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_member_include_users_ids())

    def get_can_send_message_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_send_message=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_send_message_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_send_message=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_send_message_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_send_message_exclude_users_ids())
    def get_can_send_message_include_users(self):
        return User.objects.filter(id__in=self.get_can_send_message_include_users_ids())

    def get_can_see_post_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_post=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_post_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_post=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_post_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_post_exclude_users_ids())
    def get_can_see_post_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_post_include_users_ids())

    def get_can_see_photo_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_photo=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_photo_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_photo=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_photo_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_photo_exclude_users_ids())
    def get_can_see_photo_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_photo_include_users_ids())

    def get_can_see_stat_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_stat=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_stat_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_stat=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_stat_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_stat_exclude_users_ids())
    def get_can_see_stat_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_stat_include_users_ids())

    def get_can_see_good_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_good=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_good_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_good=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_good_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_good_exclude_users_ids())
    def get_can_see_good_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_good_include_users_ids())

    def get_can_see_video_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_video=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_video_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_video=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_video_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_video_exclude_users_ids())
    def get_can_see_video_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_video_include_users_ids())

    def get_can_see_music_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_music=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_music_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_music=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_music_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_music_exclude_users_ids())
    def get_can_see_music_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_music_include_users_ids())

    def get_can_see_planner_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_planner=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_planner_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_planner=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_planner_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_planner_exclude_users_ids())
    def get_can_see_planner_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_planner_include_users_ids())

    def get_can_see_doc_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_doc=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_doc_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_doc=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_doc_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_doc_exclude_users_ids())
    def get_can_see_doc_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_doc_include_users_ids())

    def get_can_see_settings_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_settings=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_settings_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_settings=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_settings_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_settings_exclude_users_ids())
    def get_can_see_settings_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_settings_include_users_ids())

    def get_can_see_log_exclude_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_log=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_log_include_users_ids(self):
        list = self.memberships.filter(community_ie_settings__can_see_log=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_log_exclude_users(self):
        return User.objects.filter(id__in=self.get_can_see_log_exclude_users_ids())
    def get_can_see_log_include_users(self):
        return User.objects.filter(id__in=self.get_can_see_log_include_users_ids())

    def post_exclude_users(self, users, type):
        private = self.community_private2
        if type == "can_see_info":
            list = self.memberships.filter(community_ie_settings__can_see_info=2)
            for i in list:
                i.community_ie_settings.can_see_info = 0
                i.community_ie_settings.save(update_fields=["can_see_info"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_info = 2
                perm.save(update_fields=["can_see_info"])
            private.can_see_info = 5
            private.save(update_fields=["can_see_info"])
        elif type == "can_see_friend":
            list = self.memberships.filter(community_ie_settings__can_see_friend=2)
            for i in list:
                i.community_ie_settings.can_see_friend = 0
                i.community_ie_settings.save(update_fields=["can_see_friend"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_friend = 2
                perm.save(update_fields=["can_see_friend"])
            private.can_see_friend = 5
            private.save(update_fields=["can_see_friend"])
        elif type == "can_send_message":
            list = self.memberships.filter(community_ie_settings__can_send_message=2)
            for i in list:
                i.community_ie_settings.can_send_message = 0
                i.community_ie_settings.save(update_fields=["can_send_message"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_send_message = 2
                perm.save(update_fields=["can_send_message"])
            private.can_send_message = 5
            private.save(update_fields=["can_send_message"])
        elif type == "can_add_in_chat":
            list = self.memberships.filter(community_ie_settings__can_add_in_chat=2)
            for i in list:
                i.community_ie_settings.can_add_in_chat = 0
                i.community_ie_settings.save(update_fields=["can_add_in_chat"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_add_in_chat = 2
                perm.save(update_fields=["can_add_in_chat"])
            private.can_add_in_chat = 5
            private.save(update_fields=["can_add_in_chat"])
        elif type == "can_see_post":
            list = self.memberships.filter(community_ie_settings__can_see_post=2)
            for i in list:
                i.community_ie_settings.can_see_post = 0
                i.community_ie_settings.save(update_fields=["can_see_post"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_post = 2
                perm.save(update_fields=["can_see_post"])
            private.can_see_post = 5
            private.save(update_fields=["can_see_post"])
        elif type == "can_see_photo":
            list = self.memberships.filter(community_ie_settings__can_see_photo=2)
            for i in list:
                i.community_ie_settings.can_see_photo = 0
                i.community_ie_settings.save(update_fields=["can_see_photo"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_photo = 2
                perm.save(update_fields=["can_see_photo"])
            private.can_see_photo = 5
            private.save(update_fields=["can_see_photo"])
        elif type == "can_see_good":
            list = self.memberships.filter(community_ie_settings__can_see_good=2)
            for i in list:
                i.community_ie_settings.can_see_good = 0
                i.community_ie_settings.save(update_fields=["can_see_good"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_good = 2
                perm.save(update_fields=["can_see_good"])
            private.can_see_good = 5
            private.save(update_fields=["can_see_good"])
        elif type == "can_see_video":
            list = self.memberships.filter(community_ie_settings__can_see_video=2)
            for i in list:
                i.community_ie_settings.can_see_video = 0
                i.community_ie_settings.save(update_fields=["can_see_video"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_video = 2
                perm.save(update_fields=["can_see_video"])
            private.can_see_video = 5
            private.save(update_fields=["can_see_video"])
        elif type == "can_see_music":
            list = self.memberships.filter(community_ie_settings__can_see_music=2)
            for i in list:
                i.community_ie_settings.can_see_music = 0
                i.community_ie_settings.save(update_fields=["can_see_music"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_music = 2
                perm.save(update_fields=["can_see_music"])
            private.can_see_music = 5
            private.save(update_fields=["can_see_music"])
        elif type == "can_see_planner":
            list = self.memberships.filter(community_ie_settings__can_see_planner=2)
            for i in list:
                i.community_ie_settings.can_see_planner = 0
                i.community_ie_settings.save(update_fields=["can_see_planner"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_planner = 2
                perm.save(update_fields=["can_see_planner"])
            private.can_see_planner = 5
            private.save(update_fields=["can_see_planner"])
        elif type == "can_see_doc":
            list = self.memberships.filter(community_ie_settings__can_see_doc=2)
            for i in list:
                i.community_ie_settings.can_see_doc = 0
                i.community_ie_settings.save(update_fields=["can_see_doc"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_doc = 2
                perm.save(update_fields=["can_see_doc"])
            private.can_see_doc = 5
            private.save(update_fields=["can_see_doc"])
        elif type == "can_see_settings":
            list = self.memberships.filter(community_ie_settings__can_see_settings=2)
            for i in list:
                i.community_ie_settings.can_see_settings = 0
                i.community_ie_settings.save(update_fields=["can_see_settings"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_settings = 2
                perm.save(update_fields=["can_see_settings"])
            private.can_see_settings = 5
            private.save(update_fields=["can_see_settings"])
        elif type == "can_see_log":
            list = self.memberships.filter(community_ie_settings__can_see_log=2)
            for i in list:
                i.community_ie_settings.can_see_log = 0
                i.community_ie_settings.save(update_fields=["can_see_log"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_log = 2
                perm.save(update_fields=["can_see_log"])
            private.can_see_log = 5
            private.save(update_fields=["can_see_log"])
        elif type == "can_see_stat":
            list = self.memberships.filter(community_ie_settings__can_see_stat=2)
            for i in list:
                i.community_ie_settings.can_see_stat = 0
                i.community_ie_settings.save(update_fields=["can_see_stat"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_stat = 2
                perm.save(update_fields=["can_see_stat"])
            private.can_see_stat = 5
            private.save(update_fields=["can_see_stat"])

    def post_include_users(self, users, type):
        private = self.community_private2
        if type == "can_see_info":
            list = self.memberships.filter(community_ie_settings__can_see_info=1)
            for i in list:
                i.community_ie_settings.can_see_info = 0
                i.community_ie_settings.save(update_fields=["can_see_info"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_info = 1
                perm.save(update_fields=["can_see_info"])
            private.can_see_info = 6
            private.save(update_fields=["can_see_info"])
        elif type == "can_see_member":
            list = self.memberships.filter(community_ie_settings__can_see_member=1)
            for i in list:
                i.community_ie_settings.can_see_member = 0
                i.community_ie_settings.save(update_fields=["can_see_member"])
            for user_id in users:
                member = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=member.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=member.pk)
                perm.can_see_member = 1
                perm.save(update_fields=["can_see_member"])
            private.can_see_member = 6
            private.save(update_fields=["can_see_member"])
        elif type == "can_send_message":
            list = self.memberships.filter(community_ie_settings__can_send_message=1)
            for i in list:
                i.community_ie_settings.can_send_message = 0
                i.community_ie_settings.save(update_fields=["can_send_message"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_send_message = 1
                perm.save(update_fields=["can_send_message"])
            private.can_send_message = 6
            private.save(update_fields=["can_send_message"])
        elif type == "can_see_post":
            list = self.memberships.filter(community_ie_settings__can_see_post=1)
            for i in list:
                i.community_ie_settings.can_see_post = 0
                i.community_ie_settings.save(update_fields=["can_see_post"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_post = 1
                perm.save(update_fields=["can_see_post"])
            private.can_see_post = 6
            private.save(update_fields=["can_see_post"])
        elif type == "can_see_photo":
            list = self.memberships.filter(community_ie_settings__can_see_photo=1)
            for i in list:
                i.community_ie_settings.can_see_photo = 0
                i.community_ie_settings.save(update_fields=["can_see_photo"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_photo = 1
                perm.save(update_fields=["can_see_photo"])
            private.can_see_photo = 6
            private.save(update_fields=["can_see_photo"])
        elif type == "can_see_good":
            list = self.memberships.filter(community_ie_settings__can_see_good=1)
            for i in list:
                i.community_ie_settings.can_see_good = 0
                i.community_ie_settings.save(update_fields=["can_see_good"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_good = 1
                perm.save(update_fields=["can_see_good"])
            private.can_see_good = 6
            private.save(update_fields=["can_see_good"])
        elif type == "can_see_video":
            list = self.memberships.filter(community_ie_settings__can_see_video=1)
            for i in list:
                i.community_ie_settings.can_see_video = 0
                i.community_ie_settings.save(update_fields=["can_see_video"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_video = 1
                perm.save(update_fields=["can_see_video"])
            private.can_see_video = 6
            private.save(update_fields=["can_see_video"])
        elif type == "can_see_music":
            list = self.memberships.filter(community_ie_settings__can_see_music=1)
            for i in list:
                i.community_ie_settings.can_see_music = 0
                i.community_ie_settings.save(update_fields=["can_see_music"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_music = 1
                perm.save(update_fields=["can_see_music"])
            private.can_see_music = 6
            private.save(update_fields=["can_see_music"])
        elif type == "can_see_planner":
            list = self.memberships.filter(community_ie_settings__can_see_planner=1)
            for i in list:
                i.community_ie_settings.can_see_planner = 0
                i.community_ie_settings.save(update_fields=["can_see_planner"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_planner = 1
                perm.save(update_fields=["can_see_planner"])
            private.can_see_planner = 6
            private.save(update_fields=["can_see_planner"])
        elif type == "can_see_doc":
            list = self.memberships.filter(community_ie_settings__can_see_doc=1)
            for i in list:
                i.community_ie_settings.can_see_doc = 0
                i.community_ie_settings.save(update_fields=["can_see_doc"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_doc = 1
                perm.save(update_fields=["can_see_doc"])
            private.can_see_doc = 6
            private.save(update_fields=["can_see_doc"])
        elif type == "can_see_settings":
            list = self.memberships.filter(community_ie_settings__can_see_settings=1)
            for i in list:
                i.community_ie_settings.can_see_settings = 0
                i.community_ie_settings.save(update_fields=["can_see_settings"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_settings = 1
                perm.save(update_fields=["can_see_settings"])
            private.can_see_settings = 6
            private.save(update_fields=["can_see_settings"])
        elif type == "can_see_log":
            list = self.memberships.filter(community_ie_settings__can_see_log=1)
            for i in list:
                i.community_ie_settings.can_see_log = 0
                i.community_ie_settings.save(update_fields=["can_see_log"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_log = 1
                perm.save(update_fields=["can_see_log"])
            private.can_see_log = 6
            private.save(update_fields=["can_see_log"])
        elif type == "can_see_stat":
            list = self.memberships.filter(community_ie_settings__can_see_stat=1)
            for i in list:
                i.community_ie_settings.can_see_stat = 0
                i.community_ie_settings.save(update_fields=["can_see_stat"])
            for user_id in users:
                friend = self.memberships.filter(user_id=user_id).first()
                try:
                    perm = CommunityMemberPerm.objects.get(user_id=friend.pk)
                except:
                    perm = CommunityMemberPerm.objects.create(user_id=friend.pk)
                perm.can_see_stat = 1
                perm.save(update_fields=["can_see_stat"])
            private.can_see_stat = 6
            private.save(update_fields=["can_see_stat"])


class CommunityMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='communities_memberships', null=False, blank=False, verbose_name="Члены сообщества")
    community = models.ForeignKey(Community, db_index=False, on_delete=models.CASCADE, related_name='memberships', null=False, blank=False, verbose_name="Сообщество")
    is_administrator = models.BooleanField(default=False, verbose_name="Это администратор")
    is_moderator = models.BooleanField(default=False, verbose_name="Это модератор")
    is_editor = models.BooleanField(default=False, verbose_name="Это редактор")
    is_advertiser = models.BooleanField(default=False, verbose_name="Это рекламодатель")
    created = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Создано")
    visited = models.PositiveIntegerField(default=0, verbose_name="Количество визитов")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_membership(cls, user, community, is_administrator=False, is_editor=False, is_advertiser=False, is_moderator=False):
        community.add_news_subscriber_in_main_list(user.pk)
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
        ordering = ["-visited"]


class CommunityMemberPerm(models.Model):
    """ связь с таблицей подписчиков user. Появляется после ее инициирования, когда подписчик сообщества
        получит какое либо исключение или включение для какой-либо категории.
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

    user = models.OneToOneField(CommunityMembership, null=True, blank=True, on_delete=models.CASCADE, related_name='community_ie_settings', verbose_name="Подписчик сообщества")

    can_see_info = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит информацию профиля")
    can_see_member = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит подписчиков")
    can_send_message = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто пишет сообщения")
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

    can_add_post = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет к себе записи и списки")
    can_see_photo = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет к себе фото и списки")
    can_see_good = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет к себе товары и списки")
    can_see_video = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет к себе видео и списки")
    can_see_planner = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет к себе рабочие пространства и доски")
    can_see_doc = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет к себе документы и списки")
    can_see_music = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто добавляет к себе музыку и списки")

    can_create_post = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает записи и списки, работает с ними")
    can_create_photo = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает фото и списки, работает с ними")
    can_create_good = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает товары и списки, работает с ними")
    can_create_video = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает видео и списки, работает с ними")
    can_create_planner = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает рабочие пространства и доски, работает с ними")
    can_create_doc = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает документы и списки, работает с ними")
    can_create_music = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает музыку и списки, работает с ними")

    class Meta:
        verbose_name = 'Исключения/Включения подписчика'
        verbose_name_plural = 'Исключения/Включения подписчиков'
        index_together = [('id', 'user'),]

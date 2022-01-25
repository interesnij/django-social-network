import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit
from imagekit.models import ProcessedImageField
from video.helpers import upload_to_video_directory, validate_file_extension
from django.db.models import Q
from common.model.other import Stickers


class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_videos_count(self):
        return self.video_category.filter(is_deleted=True).values("pk").count()

    def is_video_in_category(self, track_id):
        self.video_category.filter(id=track_id).exists()

    def get_100_videos(self):
        queryset = self.video_category.filter(is_deleted=True).values("pk").count()
        return queryset[:100]

    class Meta:
        verbose_name = "Категория ролика"
        verbose_name_plural = "Категории ролика"


class VideoList(models.Model):
    MAIN, LIST, MANAGER = 'MAI','LIS','MAN'
    DELETED, DELETED_MANAGER = '_DEL','_DELM'
    CLOSED, CLOSED_MAIN, CLOSED_MANAGER = '_CLO','_CLOM','_CLOMA'
    ALL_CAN,FRIENDS,EACH_OTHER,FRIENDS_BUT,SOME_FRIENDS,MEMBERS,CREATOR,ADMINS,MEMBERS_BUT,SOME_MEMBERS = 1,2,3,4,5,6,7,8,9,10
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(MANAGER, 'Созданный персоналом'),
        (DELETED, 'Удалённый'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    PERM = (
            (ALL_CAN, 'Все пользователи'),
            (FRIENDS, 'Друзья'),
            (EACH_OTHER, 'Друзья,друзья друзей'),
            (CREATOR, 'Только я'),
            (FRIENDS_BUT, 'Друзья, кроме'),
            (SOME_FRIENDS, 'Некоторые друзья'),
            (MEMBERS, 'Подписчики'),
            (ADMINS, 'Администраторы'),
            (MEMBERS_BUT, 'Подписчики, кроме'),
            (SOME_MEMBERS, 'Некоторые подписчики'),
            )

    community = models.ForeignKey('communities.Community', related_name='video_lists_community', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    name = models.CharField(max_length=250, verbose_name="Название")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_user_creator', verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')
    count = models.PositiveIntegerField(default=0)
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")

    can_see_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит записи")
    can_see_comment = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит комментарии")
    create_el = models.PositiveSmallIntegerField(choices=PERM, default=7, verbose_name="Кто создает записи и потом с этими документами работает")
    create_comment = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто пишет комментарии")
    copy_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто может копировать")
    is_video_list = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Видеоальбом'
        verbose_name_plural = 'Видеоальбомы'

    def __str__(self):
        return self.name

    def count_items_ru(self):
        count = self.count_items()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " видеозапись"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " видеозаписи"
        else:
            return str(count) + " видеозаписей"

    def get_can_see_el_exclude_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_include_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_exclude_users_ids())
    def get_can_see_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_include_users_ids())

    def get_can_see_comment_exclude_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_comment_include_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_comment_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_comment_exclude_users_ids())
    def get_can_see_comment_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_comment_include_users_ids())

    def get_create_el_exclude_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_include_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_exclude_users_ids())
    def get_create_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_include_users_ids())

    def get_create_comment_exclude_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_comment_include_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_comment_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_comment_exclude_users_ids())
    def get_create_comment_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_comment_include_users_ids())

    def get_copy_el_exclude_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_include_users_ids(self):
        list = VideoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_copy_el_exclude_users_ids())
    def get_copy_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_copy_el_include_users_ids())

    def is_user_can_see_el(self, user_id):
        if self.community:
            if self.can_see_el == self.ALL_CAN:
                return True
            elif self.can_see_el == self.CREATOR and user_id == self.community.creator.pk:
                return True
            elif self.can_see_el == self.ADMINS and user_id in self.community.get_admins_ids():
                return True
            elif self.can_see_el == self.MEMBERS and user_id in self.community.get_members_ids():
                return True
            elif self.can_see_el == self.MEMBERS_BUT:
                return not user_id in self.get_can_see_el_exclude_users_ids()
            elif self.can_see_el == self.SOME_MEMBERS:
                return user_id in self.get_can_see_el_include_users_ids()
        else:
            if self.can_see_el == self.ALL_CAN:
                return True
            elif self.can_see_el == self.CREATOR and user_id == self.creator.pk:
                return True
            elif self.can_see_el == self.FRIENDS and user_id in self.creator.get_all_friends_ids():
                return True
            elif self.can_see_el == self.EACH_OTHER and user_id in self.creator.get_friend_and_friend_of_friend_ids():
                return True
            elif self.can_see_el == self.FRIENDS_BUT:
                return not user_id in self.get_can_see_el_exclude_users_ids()
            elif self.can_see_el == self.SOME_FRIENDS:
                return user_id in self.get_can_see_el_include_users_ids()
        return False
    def is_anon_user_can_see_el(self):
        return self.can_see_el == self.ALL_CAN

    def is_user_can_see_comment(self, user_id):
        if self.community:
            if self.can_see_comment == self.ALL_CAN:
                return True
            elif self.can_see_comment == self.CREATOR and user_id == self.community.creator.pk:
                return True
            elif self.can_see_comment == self.ADMINS and user_id in self.community.get_admins_ids():
                return True
            elif self.can_see_comment == self.MEMBERS and user_id in self.community.get_members_ids():
                return True
            elif self.can_see_comment == self.MEMBERS_BUT:
                return not user_id in self.get_can_see_comment_exclude_users_ids()
            elif self.can_see_comment == self.SOME_MEMBERS:
                return user_id in self.get_can_see_comment_include_users_ids()
        else:
            if self.can_see_comment == self.ALL_CAN:
                return True
            elif self.can_see_comment == self.CREATOR and user_id == self.creator.pk:
                return True
            elif self.can_see_comment == self.FRIENDS and user_id in self.creator.get_all_friends_ids():
                return True
            elif self.can_see_comment == self.EACH_OTHER and user_id in self.creator.get_friend_and_friend_of_friend_ids():
                return True
            elif self.can_see_comment == self.FRIENDS_BUT:
                return not user_id in self.get_can_see_comment_exclude_users_ids()
            elif self.can_see_comment == self.SOME_FRIENDS:
                return user_id in self.get_can_see_comment_include_users_ids()
        return False
    def is_anon_user_can_see_comment(self):
        return self.can_see_comment == self.ALL_CAN

    def is_user_can_create_el(self, user_id):
        if self.community:
            if self.create_el == self.ALL_CAN:
                return True
            elif self.create_el == self.CREATOR and user_id == self.community.creator.pk:
                return True
            elif self.create_el == self.ADMINS and user_id in self.community.get_admins_ids():
                return True
            elif self.create_el == self.MEMBERS and user_id in self.community.get_members_ids():
                return True
            elif self.create_el == self.MEMBERS_BUT:
                return not user_id in self.get_create_el_exclude_users_ids()
            elif self.create_el == self.SOME_MEMBERS:
                return user_id in self.get_create_el_include_users_ids()
        else:
            if self.create_el == self.ALL_CAN:
                return True
            elif self.create_el == self.CREATOR and user_id == self.creator.pk:
                return True
            elif self.create_el == self.FRIENDS and user_id in self.creator.get_all_friends_ids():
                return True
            elif self.create_el == self.EACH_OTHER and user_id in self.creator.get_friend_and_friend_of_friend_ids():
                return True
            elif self.create_el == self.FRIENDS_BUT:
                return not user_id in self.get_create_el_exclude_users_ids()
            elif self.create_el == self.SOME_FRIENDS:
                return user_id in self.get_create_el_include_users_ids()
        return False
    def is_anon_user_can_create_item(self):
        return self.create_el == self.ALL_CAN

    def is_user_can_create_comment(self, user_id):
        if self.community:
            if self.create_comment == self.ALL_CAN:
                return True
            elif self.create_comment == self.CREATOR and user_id == self.community.creator.pk:
                return True
            elif self.create_comment == self.ADMINS and user_id in self.community.get_admins_ids():
                return True
            elif self.create_comment == self.MEMBERS and user_id in self.community.get_members_ids():
                return True
            elif self.create_comment == self.MEMBERS_BUT:
                return not user_id in self.get_create_comment_exclude_users_ids()
            elif self.create_comment == self.SOME_MEMBERS:
                return user_id in self.get_create_comment_include_users_ids()
        else:
            if self.create_comment == self.ALL_CAN:
                return True
            elif self.create_comment == self.CREATOR and user_id == self.creator.pk:
                return True
            elif self.create_comment == self.FRIENDS and user_id in self.creator.get_all_friends_ids():
                return True
            elif self.create_comment == self.EACH_OTHER and user_id in self.creator.get_friend_and_friend_of_friend_ids():
                return True
            elif self.create_comment == self.FRIENDS_BUT:
                return not user_id in self.get_create_comment_exclude_users_ids()
            elif self.create_comment == self.SOME_FRIENDS:
                return user_id in self.get_create_comment_include_users_ids()
        return False
    def is_anon_user_can_create_comment(self):
        return self.create_comment == self.ALL_CAN

    def is_user_can_copy_el(self, user_id):
        if self.community:
            if self.copy_el == self.ALL_CAN:
                return True
            elif self.copy_el == self.CREATOR and user_id == self.community.creator.pk:
                return True
            elif self.copy_el == self.ADMINS and user_id in self.community.get_admins_ids():
                return True
            elif self.copy_el == self.MEMBERS and user_id in self.community.get_members_ids():
                return True
            elif self.copy_el == self.MEMBERS_BUT:
                return not user_id in self.get_copy_el_exclude_users_ids()
            elif self.copy_el == self.SOME_MEMBERS:
                return user_id in self.get_copy_el_include_users_ids()
        else:
            if self.copy_el == self.ALL_CAN:
                return True
            elif self.copy_el == self.CREATOR and user_id == self.creator.pk:
                return True
            elif self.copy_el == self.FRIENDS and user_id in self.creator.get_all_friends_ids():
                return True
            elif self.copy_el == self.EACH_OTHER and user_id in self.creator.get_friend_and_friend_of_friend_ids():
                return True
            elif self.copy_el == self.FRIENDS_BUT:
                return not user_id in self.get_copy_el_exclude_users_ids()
            elif self.copy_el == self.SOME_FRIENDS:
                return user_id in self.get_copy_el_include_users_ids()
        return False
    def is_anon_user_can_copy_el(self):
        return self.copy_el == self.ALL_CAN

    def add_in_community_collections(self, community):
        from communities.model.list import CommunityVideoListPosition
        CommunityVideoListPosition.objects.create(community=community.pk, list=self.pk, position=VideoList.get_community_lists_count(community.pk))
        self.communities.add(community)
    def remove_in_community_collections(self, community):
        from communities.model.list import CommunityVideoListPosition
        CommunityVideoListPosition.objects.get(community=community.pk, list=self.pk).delete()
        self.communities.remove(user)
    def add_in_user_collections(self, user):
        from users.model.list import UserVideoListPosition
        UserVideoListPosition.objects.create(user=user.pk, list=self.pk, position=VideoList.get_user_lists_count(user.pk))
        self.users.add(user)
    def remove_in_user_collections(self, user):
        from users.model.list import UserVideoListPosition
        UserVideoListPosition.objects.get(user=user.pk, list=self.pk).delete()
        self.users.remove(user)

    def is_not_empty(self):
        return self.video_list.filter(Q(type="PUB")|Q(type="PRI")).values("pk").exists()

    def get_items(self):
        return self.video_list.filter(type="PUB")
    def get_2_items(self):
        return self.video_list.filter(type="PUB")[:2]
    def get_2_staff_items(self):
        return self.video_list.filter(Q(type="PUB")|Q(type="PRI"))[:2]
    def get_manager_items(self):
        return self.video_list.filter(type="MAN")
    def count_items(self):
        return self.video_list.filter(Q(type="PUB")|Q(type="PRI")).values("pk").count()

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_open(self):
        return self.type == self.LIST or self.type == self.MAIN or self.type == self.MANAGER
    def is_have_edit(self):
        return self.is_list()
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in communities]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids()
    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_community_can_add_list(self, community_id):
        return self.community.pk != community_id and community_id not in self.get_communities_ids()
    def is_community_can_delete_list(self, community_id):
        return self.community.pk != community_id and community_id in self.get_communities_ids()

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        try:
            from users.model.list import UserVideoListPosition
            query = []
            lists = UserVideoListPosition.objects.filter(user=user_pk, type=1).values("list")
            for list_id in [i['list'] for i in lists]:
                list = cls.objects.get(pk=list_id)
                if list.type[0] != "_":
                    query.append(list)
            return query
        except:
            query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
            query.add(~Q(type__contains="_"), Q.AND)
            return cls.objects.filter(query)
    @classmethod
    def get_user_lists(cls, user_pk):
        try:
            from users.model.list import UserVideoListPosition
            query = []
            lists = UserVideoListPosition.objects.filter(user=user_pk, type=1).values("list")
            for list_id in [i['list'] for i in lists]:
                list = cls.objects.get(pk=list_id)
                if list.is_have_get():
                    query.append(list)
            return query
        except:
            query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
            query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
            return cls.objects.filter(query)
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk))
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        try:
            from communities.model.list import CommunityVideoListPosition
            query = []
            lists = CommunityVideoListPosition.objects.filter(community=community_pk, type=1).values("list")
            for list_id in [i['list'] for i in lists]:
                list = cls.objects.get(pk=list_id)
                if list.type[0] != "_":
                    query.append(list)
            return query
        except:
            query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
            query.add(~Q(type__contains="_"), Q.AND)
            return cls.objects.filter(query)
    @classmethod
    def get_community_lists(cls, community_pk):
        try:
            from communities.model.list import CommunityVideoListPosition
            query = []
            lists = CommunityVideoListPosition.objects.filter(community=community_pk, type=1).values("list")
            for list_id in [i['list'] for i in lists]:
                list = cls.objects.get(pk=list_id)
                if list.is_have_get():
                    query.append(list)
            return query
        except:
            query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
            query.add(Q(Q(type="LIS")|Q(type="MAI")), Q.AND)
            return cls.objects.filter(query)
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(Q(community_id=community_pk)|Q(communities__id=community_pk))
        query.add(~Q(type__contains="_"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def create_list(cls, creator, name, description, community,can_see_el,can_see_comment,create_el,create_comment,copy_el,\
        can_see_el_users,can_see_comment_users,create_el_users,create_comment_users,copy_el_users):
        from common.processing.video import get_video_list_processing

        list = cls.objects.create(creator=creator,name=name,description=description, community=community,can_see_el=can_see_el,can_see_comment=can_see_comment,create_el=create_el,create_comment=create_comment,copy_el=copy_el)
        get_video_list_processing(list, VideoList.LIST)
        if community:
            from communities.model.list import CommunityVideoListPosition
            CommunityVideoListPosition.objects.create(community=community.pk, list=list.pk, position=VideoList.get_community_lists_count(community.pk))
        else:
            from users.model.list import UserVideoListPosition
            UserVideoListPosition.objects.create(user=creator.pk, list=list.pk, position=VideoList.get_user_lists_count(creator.pk))

        if can_see_el == 4 or can_see_el == 9:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])

        if can_see_comment == 4 or can_see_comment == 9:
            if can_see_comment_users:
                for user_id in can_see_comment_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_comment = 2
                    perm.save(update_fields=["can_see_comment"])
            else:
                list.can_see_comment = 7
                list.save(update_fields=["can_see_comment"])
        elif can_see_comment == 5 or can_see_comment == 10:
            if can_see_comment_users:
                for user_id in can_see_comment_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_comment = 1
                    perm.save(update_fields=["can_see_comment"])
            else:
                list.can_see_comment = 7
                list.save(update_fields=["can_see_comment"])

        if create_el == 4 or create_el == 9:
            if create_el_users:
                for user_id in create_el_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                for user_id in create_el_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])

        if create_comment == 4 or create_comment == 9:
            if create_comment_users:
                for user_id in create_comment_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_comment = 2
                    perm.save(update_fields=["create_comment"])
            else:
                list.create_comment = 7
                list.save(update_fields=["create_comment"])
        elif create_comment == 5 or create_comment == 10:
            if create_comment_users:
                for user_id in create_comment_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_comment = 1
                    perm.save(update_fields=["create_comment"])
            else:
                list.create_comment = 7
                list.save(update_fields=["create_comment"])

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                list.copy_el = 7
                list.save(update_fields=["copy_el"])
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = VideoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_copy = 1
                    perm.save(update_fields=["can_copy"])
            else:
                list.copy_el = 7
                list.save(update_fields=["copy_el"])

        return list

    def edit_list(self, name, description,can_see_el,can_see_comment,create_el,create_comment,copy_el,\
        can_see_el_users,can_see_comment_users,create_el_users,create_comment_users,copy_el_users):

        self.name = name
        self.description = description
        self.can_see_el = can_see_el
        self.can_see_comment = can_see_comment
        self.create_el = create_el
        self.create_comment = create_comment
        self.copy_el = copy_el
        if can_see_el == 4 or can_see_el == 9:
            if can_see_el_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7

        if can_see_comment == 4 or can_see_comment == 9:
            if can_see_comment_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(can_see_comment=0)
                for user_id in can_see_comment_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_comment = 2
                    perm.save(update_fields=["can_see_comment"])
            else:
                self.can_see_comment = 7
        elif can_see_comment == 5 or can_see_comment == 10:
            if can_see_comment_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(can_see_comment=0)
                for user_id in can_see_comment_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_comment = 1
                    perm.save(update_fields=["can_see_comment"])
            else:
                self.can_see_comment = 7

        if create_el == 4 or create_el == 9:
            if create_el_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7

        if create_comment == 4 or create_comment == 9:
            if create_comment_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(create_comment=0)
                for user_id in create_comment_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_comment = 2
                    perm.save(update_fields=["create_comment"])
            else:
                self.create_comment = 7
        elif create_comment == 5 or create_comment == 10:
            if create_comment_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(create_comment=0)
                for user_id in create_comment_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_comment = 1
                    perm.save(update_fields=["create_comment"])
            else:
                self.create_comment = 7

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                VideoListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = VideoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 1
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7

        self.save()
        return self

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = VideoList.DELETED
        elif self.type == "MAN":
            self.type = VideoList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityVideoListPosition
            CommunityVideoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserVideoListPosition
            UserVideoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = VideoList.LIST
        elif self.type == "_DELM":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityVideoListPosition
            CommunityVideoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserVideoListPosition
            UserVideoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = VideoList.CLOSED
        elif self.type == "MAI":
            self.type = VideoList.CLOSED_MAIN
        elif self.type == "MAN":
            self.type = VideoList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityVideoListPosition
            CommunityVideoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserVideoListPosition
            UserVideoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = VideoList.LIST
        elif self.type == "_CLOM":
            self.type = VideoList.MAIN
        elif self.type == "_CLOM":
            self.type = VideoList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityVideoListPosition
            CommunityVideoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserVideoListPosition
            UserVideoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VIL", object_id=self.pk, verb="ITE").update(status="R")


class Video(models.Model):
    PUBLISHED, MANAGER, DELETED, CLOSED = 'PUB','MAN','_DEL','_CLO'
    DELETED_MANAGER, CLOSED_MANAGER = '_DELM','_CLOM'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    image = ProcessedImageField(format='JPEG',
                                options={'quality': 90},
                                upload_to=upload_to_video_directory,
                                processors=[ResizeToFit(width=500, upscale=False)],
                                verbose_name="Обложка")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=500, blank=True, verbose_name="Описание")
    title = models.CharField(max_length=255, verbose_name="Название")
    uri = models.CharField(max_length=255, verbose_name="Ссылка на видео")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    list = models.ForeignKey(VideoList, on_delete=models.SET_NULL, related_name='video_list', blank=True, null=True)
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="video_creator", on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(choices=TYPE, max_length=5)
    file = models.FileField(blank=True, upload_to=upload_to_video_directory, validators=[validate_file_extension], verbose_name="Видеозапись")
    community = models.ForeignKey('communities.Community', related_name='video_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")
    order = models.PositiveIntegerField(default=0)
    is_video = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Видео-ролики"
        verbose_name_plural = "Видео-ролики"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-order"]

    def __str__(self):
        return self.title

    def count_reposts(self):
        if self.repost == 0:
            return ''
        else:
            return self.repost

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return "/static/images/no_img/list.jpg"

    def plus_likes(self, count):
        self.like += count
        return self.save(update_fields=['like'])
    def minus_likes(self, count):
        self.like -= count
        return self.save(update_fields=['like'])
    def plus_dislikes(self, count):
        self.dislike += count
        return self.save(update_fields=['dislike'])
    def minus_dislikes(self, count):
        self.dislike -= count
        return self.save(update_fields=['dislike'])
    def plus_comments(self, count):
        self.comment += count
        return self.save(update_fields=['comment'])
    def minus_comments(self, count):
        self.comment -= count
        return self.save(update_fields=['comment'])
    def plus_views(self, count):
        self.view += count
        return self.save(update_fields=['view'])
    def minus_views(self, count):
        self.view -= count
        return self.save(update_fields=['view'])
    def plus_reposts(self, count):
        self.repost += count
        return self.save(update_fields=['repost'])
    def minus_reposts(self, count):
        self.repost -= count
        return self.save(update_fields=['repost'])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def likes(self):
        from common.model.votes import VideoVotes
        return VideoVotes.objects.filter(parent=self, vote__gt=0)

    def window_likes(self):
        from common.model.votes import VideoVotes
        return VideoVotes.objects.filter(parent=self, vote__gt=0)[0:6]

    def dislikes(self):
        from common.model.votes import VideoVotes
        return VideoVotes.objects.filter(parent=self, vote__lt=0)

    def window_dislikes(self):
        from common.model.votes import VideoVotes
        return VideoVotes.objects.filter(parent=self, vote__lt=0)[0:6]

    def visits_count_ru(self):
        count = self.all_visits_count()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " просмотр"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " просмотра"
        else:
            return str(count) + " просмотров"

    def all_visits_count(self):
        from stst.models import VideoNumbers
        return VideoNumbers.objects.filter(video=self.pk).values('pk').count()

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''

    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''

    def count_comments(self):
        if self.comment > 0:
            return self.comment
        else:
            return ''

    def get_comments(self):
        return VideoComment.objects.filter(video_id=self.pk, parent__isnull=True)

    @classmethod
    def create_video(cls, creator, image, title, file, uri, description, list, comments_enabled, votes_on, community):
        from common.processing.video import get_video_processing

        list.count += 1
        list.save(update_fields=["count"])
        video = cls.objects.create(creator=creator,image=image, order=list.count,list=list,title=title,file=file,uri=uri,description=description,comments_enabled=comments_enabled,votes_on=votes_on)

        get_video_processing(video, Video.PUBLISHED)
        if community:
            from common.notify.progs import community_send_notify, community_send_wall
            from notify.models import Notify, Wall

            Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="VID", object_id=video.pk, verb="ITE")
            community_send_wall(video.pk, creator.pk, community.pk, None, "create_c_video_wall")
            for user_id in community.get_member_for_notify_ids():
                Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                community_send_notify(video.pk, creator.pk, user_id, community.pk, None, "create_c_video_notify")
            community.plus_videos(1)
        else:
            from common.notify.progs import user_send_notify, user_send_wall
            from notify.models import Notify, Wall

            Wall.objects.create(creator_id=creator.pk, type="VID", object_id=video.pk, verb="ITE")
            user_send_wall(video.pk, None, "create_u_video_wall")
            for user_id in creator.get_user_main_news_ids():
                Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="VID", object_id=video.pk, verb="ITE")
                user_send_notify(video.pk, creator.pk, user_id, None, "create_u_video_notify")
            creator.plus_videos(1)
        return video

    def edit_video(self, title, file, uri, description, lists, comments_enabled, votes_on):
        from common.processing.video import get_video_processing

        self.title = title
        self.file = file
        self.uri = uri
        if self.list.pk != list.pk:
            self.list.count -= 1
            self.list.save(update_fields=["count"])
            list.count += 1
            list.save(update_fields=["count"])
        self.list = list
        self.description = description
        self.comments_enabled = comments_enabled
        self.votes_on = votes_on
        return self.save()

    def get_uri(self):
        if self.file:
            return self.file.url
        else:
            return self.uri

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Video.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Video.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Video.DELETED
        elif self.type == "MAN":
            self.type = Video.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_videos(1)
        else:
            self.creator.minus_videos(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Video.PUBLISHED
        elif self.type == "_DELM":
            self.type = Video.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_videos(1)
        else:
            self.creator.plus_videos(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Video.CLOSED
        elif self.type == "MAN":
            self.type = Video.CLOSED_MANAGER
        self.save(update_fields=['type'])
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if community:
            community.minus_videos(1)
        else:
            self.creator.minus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Video.PUBLISHED
        elif self.type == "_CLOM":
            self.type = Video.MANAGER
        self.save(update_fields=['type'])
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if community:
            community.plus_videos(1)
        else:
            self.creator.plus_videos(1)
        if Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="VID", object_id=self.pk, verb="ITE").update(status="R")

    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"


class VideoComment(models.Model):
    EDITED, PUBLISHED, DRAFT = 'EDI', 'PUB', '_DRA'
    DELETED, EDITED_DELETED = '_DEL', '_DELE'
    CLOSED, EDITED_CLOSED = '_CLO', '_CLOE'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(DRAFT, 'Черновик'),
        (DELETED, 'Удалённый'), (EDITED_DELETED, 'Удалённый изменённый'),
        (CLOSED, 'Закрытый менеджером'), (EDITED_CLOSED, 'Закрытый изменённый'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='video_comment_replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    item = models.ForeignKey(Video, on_delete=models.CASCADE, blank=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип альбома")
    sticker = models.ForeignKey(Stickers, blank=True, null=True, on_delete=models.CASCADE, related_name="+")

    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name = "комментарий к ролику"
        verbose_name_plural = "комментарии к ролику"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_item(self):
        if self.parent:
            return self.parent.item
        else:
            return self.item

    def all_visits_count(self):
        from stst.models import VideoNumbers
        return VideoNumbers.objects.filter(video=self.pk).values('pk').count()

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return self.video_comment_replies.filter(Q(type=VideoComment.EDITED)|Q(type=VideoComment.PUBLISHED)).only("pk")

    def count_replies(self):
        return self.video_comment_replies.filter(Q(type=VideoComment.EDITED)|Q(type=VideoComment.PUBLISHED)).values("pk").count()

    def likes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__gt=0)

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''

    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''

    def window_likes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__gt=0)[0:6]

    def dislikes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__lt=0)

    def window_dislikes(self):
        return VideoCommentVotes.objects.filter(item=self, vote__lt=0)[0:6]

    @classmethod
    def create_comment(cls, commenter, attach, item, parent, text, community, sticker):
        from common.processing_2 import get_text_processing

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        if sticker:
            comment = VideoComment.objects.create(commenter=commenter, sticker_id=sticker, parent=parent, item=item)
        else:
            comment = VideoComment.objects.create(commenter=commenter, attach=_attach, parent=parent, item=item, text=get_text_processing(text))
        item.comment += 1
        item.save(update_fields=["comment"])
        if parent:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
                community_wall(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
                user_wall(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "REP")
        else:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
                community_wall(comment.commenter, community, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
                user_wall(comment.commenter, None, comment.pk, "VIDC", "u_video_comment_notify", "COM")
        return comment

    def edit_comment(self, attach, text):
        from common.processing_2 import get_text_processing
        if not text and not attach:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Нет текста или прикрепленных элементов")

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        _text = get_text_processing(text)
        self.attach = _attach
        self.text = _text
        self.type = VideoComment.EDITED
        self.save()
        return self

    def count_replies_ru(self):
        count = self.count_replies()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " ответ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " ответа"
        else:
            return str(count) + " ответов"

    def get_attach(self, user):
        from common.attach.comment_attach import get_comment_attach
        return get_comment_attach(self, user)

    def send_like(self, user, community):
        import json
        from common.model.votes import VideoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = VideoCommentVotes.objects.get(item=self, user=user)
            if item.vote != VideoCommentVotes.LIKE:
                item.vote = VideoCommentVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=self, user=user, vote=VideoCommentVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LRE")
                    community_wall(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "LRE")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "LCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LCO")
                    community_wall(user, community, None, self.pk, "POSC", "u_video_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "LCO")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "LCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import VideoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = VideoCommentVotes.objects.get(item=self, user=user)
            if item.vote != VideoCommentVotes.DISLIKE:
                item.vote = VideoCommentVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except VideoCommentVotes.DoesNotExist:
            VideoCommentVotes.objects.create(item=self, user=user, vote=VideoCommentVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DRE")
                    community_wall(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "DRE")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                    community_wall(user, community, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
                    user_wall(user, None, self.pk, "VIDC", "u_video_comment_notify", "DCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = VideoComment.DELETED
        elif self.type == "EDI":
            self.type = VideoComment.EDITED_DELETED
        self.save(update_fields=['type'])
        for list in self.get_lists():
            list.count -= 1
            list.save(update_fields=["count"])
        if self.parent:
            self.parent.item.comment -= 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.item.comment -= 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = VideoComment.PUBLISHED
        elif self.type == "_DELE":
            self.type = VideoComment.EDITED
        self.save(update_fields=['type'])
        for list in self.get_lists():
            list.count += 1
            list.save(update_fields=["count"])
        if self.parent:
            self.parent.item.comment += 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.item.comment += 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = VideoComment.CLOSED
        elif self.type == "EDI":
            self.type = VideoComment.EDITED_CLOSED
        self.save(update_fields=['type'])
        for list in self.get_lists():
            list.count -= 1
            list.save(update_fields=["count"])
        if self.parent:
            self.parent.item.comment -= 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.item.comment -= 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = VideoComment.PUBLISHED
        elif self.type == "_CLOE":
            self.type = VideoComment.EDITED
        self.save(update_fields=['type'])
        for list in self.get_lists():
            list.count += 1
            list.save(update_fields=["count"])
        if self.parent:
            self.parent.item.comment += 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.item.comment += 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="VIDC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="VIDC", object_id=self.pk, verb="COM").update(status="R")

    def get_edit_attach(self, user):
        from common.attach.comment_attach import get_comment_edit
        return get_comment_edit(self, user)

    def get_format_text(self):
        from common.utils import hide_text
        return hide_text(self.text)


class VideoListPerm(models.Model):
    """ включения и исключения для пользователей касательно конкретного списка записей
        1. YES_ITEM - может соверщать описанные действия
        2. NO_ITEM - не может соверщать описанные действия
    """
    NO_VALUE, YES_ITEM, NO_ITEM, TEST = 0, 1, 2, 3
    ITEM = (
        (YES_ITEM, 'Может иметь действия с элементом'),
        (NO_ITEM, 'Не может иметь действия с элементом'),
        (NO_VALUE, 'Нет значения'),
    )

    list = models.ForeignKey(VideoList, related_name='+', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Список записей")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=False, verbose_name="Пользователь")

    can_see_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит список/видеозаписи")
    can_see_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комментарии")
    create_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает видеозаписи")
    create_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комментарии")
    can_copy = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто может добавлять список/видеозаписи себе")

    class Meta:
        verbose_name = 'Исключения/Включения друга'
        verbose_name_plural = 'Исключения/Включения друзей'

    @classmethod
    def get_or_create_perm(cls, list_id, user_id, ):
        if cls.objects.filter(list_id=list_id, user_id=user_id).exists():
            return cls.objects.get(list_id=list_id, user_id=user_id)
        else:
            perm = cls.objects.create(list_id=list_id, user_id=user_id)
            return perm

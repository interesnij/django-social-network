import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q
from gallery.helpers import upload_to_photo_directory
from common.model.other import Stickers


class PhotoList(models.Model):
    MAIN, LIST, WALL, AVATAR, MANAGER = 'MAI', 'LIS', 'WAL', 'AVA', 'MAN'
    DELETED, DELETED_MANAGER = '_DEL', '_DELM'
    CLOSED, CLOSED_MAIN, CLOSED_MANAGER, CLOSED_WALL, CLOSED_AVATAR = '_CLO', '_CLOM', '_CLOMA', '_CLOW', '_CLOA'
    ALL_CAN,FRIENDS,EACH_OTHER,FRIENDS_BUT,SOME_FRIENDS,MEMBERS,CREATOR,ADMINS,MEMBERS_BUT,SOME_MEMBERS = 1,2,3,4,5,6,7,8,9,10
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(WALL, 'Фото со стены'),(AVATAR, 'Фото со страницы'),(MANAGER, 'Созданный персоналом'),
        (DELETED, 'Удалённый'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),(CLOSED_WALL, 'Закрытый со стены'),(CLOSED_AVATAR, 'Закрытый со страницы'),
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

    community = models.ForeignKey('communities.Community', related_name='photo_lists_community', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    cover_photo = models.ForeignKey('Photo', on_delete=models.SET_NULL, related_name='+', blank=True, null=True, verbose_name="Обожка")
    type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип альбома")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_list_creator', null=False, blank=False, verbose_name="Создатель")

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
    is_photo_list = models.BooleanField(default=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фотоальбом'
        verbose_name_plural = 'Фотоальбомы'

    def __str__(self):
        return self.name

    def get_can_see_el_exclude_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_include_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_exclude_users_ids())
    def get_can_see_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_include_users_ids())

    def get_can_see_comment_exclude_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_comment_include_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_comment_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_comment_exclude_users_ids())
    def get_can_see_comment_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_comment_include_users_ids())

    def get_create_el_exclude_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_include_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_exclude_users_ids())
    def get_create_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_include_users_ids())

    def get_create_comment_exclude_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_comment_include_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_comment_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_comment_exclude_users_ids())
    def get_create_comment_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_comment_include_users_ids())

    def get_copy_el_exclude_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_include_users_ids(self):
        list = PhotoListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
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
        from communities.model.list import CommunityPhotoListPosition
        CommunityPhotoListPosition.objects.create(community=community.pk, list=self.pk, position=PhotoList.get_community_lists_count(community.pk))
        self.communities.add(community)
    def remove_in_community_collections(self, community):
        from communities.model.list import CommunityPhotoListPosition
        try:
            CommunityPhotoListPosition.objects.get(community=community.pk, list=self.pk).delete()
        except:
            pass
        self.communities.remove(user)
    def add_in_user_collections(self, user):
        from users.model.list import UserPhotoListPosition
        UserPhotoListPosition.objects.create(user=user.pk, list=self.pk, position=PhotoList.get_user_lists_count(user.pk))
        self.users.add(user)
    def remove_in_user_collections(self, user):
        from users.model.list import UserPhotoListPosition
        try:
            UserPhotoListPosition.objects.get(user=user.pk, list=self.pk).delete()
        except:
            pass
        self.users.remove(user)

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

    def is_avatar(self):
        return self.type == self.AVATAR
    def is_wall(self):
        return self.type == self.WALL
    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_have_edit(self):
        return self.is_list()
    def is_open(self):
        return self.type[0] != "_"
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_suspended(self):
        return False

    def get_cover_photo(self):
        if self.cover_photo:
            return self.cover_photo.file.url
        elif self.photo_list.filter(type="PUB").exists():
            return self.photo_list.filter(type="PUB").first().file.url
        else:
            return "/static/images/no_img/list.jpg"

    def get_first_photo(self):
        return self.photo_list.exclude(type__contains="_").first()

    def get_items(self):
        return self.photo_list.filter(type="PUB")
    def get_6_items(self):
        return self.photo_list.filter(type="PUB")[:6]
    def get_6_staff_items(self):
        return self.photo_list.exclude(type__contains="_")[:6]
    def count_items(self):
        try:
            return self.photo_list.filter(type="PUB").values("pk").count()
        except:
            return 0
    def count_items_ru(self):
        count = self.count_items()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " фотография"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " фотографии"
        else:
            return str(count) + " фотографий"

    def is_not_empty(self):
        return self.photo_list.filter(type="PUB").values("pk").exists()

    def is_item_in_list(self, item_id):
        return self.photo_list.filter(pk=item_id).values("pk").exists()

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        try:
            from users.model.list import UserPhotoListPosition
            query = []
            lists = UserPhotoListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from users.model.list import UserPhotoListPosition
            query = []
            lists = UserPhotoListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from communities.model.list import CommunityPhotoListPosition
            query = []
            lists = CommunityPhotoListPosition.objects.filter(community=community_pk, type=1).values("list")
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
            from communities.model.list import CommunityPhotoListPosition
            query = []
            lists = CommunityPhotoListPosition.objects.filter(community=community_pk, type=1).values("list")
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
    def create_list(cls, creator, name, description,community,can_see_el,can_see_comment,create_el,create_comment,copy_el,\
        can_see_el_users,can_see_comment_users,create_el_users,create_comment_users,copy_el_users):
        from common.processing.photo import get_photo_list_processing

        list = cls.objects.create(creator=creator,name=name,description=description,community=community,can_see_el=can_see_el,can_see_comment=can_see_comment,create_el=create_el,create_comment=create_comment,copy_el=copy_el)
        get_photo_list_processing(list, PhotoList.LIST)
        if community:
            from communities.model.list import CommunityPhotoListPosition
            CommunityPhotoListPosition.objects.create(community=community.pk, list=list.pk, position=PhotoList.get_community_lists_count(community.pk))
        else:
            from users.model.list import UserPhotoListPosition
            UserPhotoListPosition.objects.create(user=creator.pk, list=list.pk, position=PhotoList.get_user_lists_count(creator.pk))

        if can_see_el == 4 or can_see_el == 9:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])

        if can_see_comment == 4 or can_see_comment == 9:
            if can_see_comment_users:
                for user_id in can_see_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_comment = 2
                    perm.save(update_fields=["can_see_comment"])
            else:
                list.can_see_comment = 7
                list.save(update_fields=["can_see_comment"])
        elif can_see_comment == 5 or can_see_comment == 10:
            if can_see_comment_users:
                for user_id in can_see_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_comment = 1
                    perm.save(update_fields=["can_see_comment"])
            else:
                list.can_see_comment = 7
                list.save(update_fields=["can_see_comment"])

        if create_el == 4 or create_el == 9:
            if create_el_users:
                for user_id in create_el_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                for user_id in create_el_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])

        if create_comment == 4 or create_comment == 9:
            if create_comment_users:
                for user_id in create_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_comment = 2
                    perm.save(update_fields=["create_comment"])
            else:
                list.create_comment = 7
                list.save(update_fields=["create_comment"])
        elif create_comment == 5 or create_comment == 10:
            if create_comment_users:
                for user_id in create_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_comment = 1
                    perm.save(update_fields=["create_comment"])
            else:
                list.create_comment = 7
                list.save(update_fields=["create_comment"])

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                list.copy_el = 7
                list.save(update_fields=["copy_el"])
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = PhotoListPerm.get_or_create_perm(list.pk, user_id)
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
                PhotoListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7

        if can_see_comment == 4 or can_see_comment == 9:
            if can_see_comment_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(can_see_comment=0)
                for user_id in can_see_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_comment = 2
                    perm.save(update_fields=["can_see_comment"])
            else:
                self.can_see_comment = 7
        elif can_see_comment == 5 or can_see_comment == 10:
            if can_see_comment_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(can_see_comment=0)
                for user_id in can_see_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_comment = 1
                    perm.save(update_fields=["can_see_comment"])
            else:
                self.can_see_comment = 7

        if create_el == 4 or create_el == 9:
            if create_el_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7

        if create_comment == 4 or create_comment == 9:
            if create_comment_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(create_comment=0)
                for user_id in create_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_comment = 2
                    perm.save(update_fields=["create_comment"])
            else:
                self.create_comment = 7
        elif create_comment == 5 or create_comment == 10:
            if create_comment_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(create_comment=0)
                for user_id in create_comment_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_comment = 1
                    perm.save(update_fields=["create_comment"])
            else:
                self.create_comment = 7

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                PhotoListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = PhotoListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 1
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7

        self.save()
        return self

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PhotoList.DELETED
        elif self.type == "MAN":
            self.type = PhotoList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPhotoListPosition
            CommunityPhotoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserPhotoListPosition
            UserPhotoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = PhotoList.LIST
        elif self.type == "_DELM":
            self.type = PhotoList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPhotoListPosition
            CommunityPhotoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserPhotoListPosition
            UserPhotoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PhotoList.CLOSED
        elif self.type == "MAI":
            self.type = PhotoList.CLOSED_MAIN
        elif self.type == "MAN":
            self.type = PhotoList.CLOSED_MANAGER
        elif self.type == "AVA":
            self.type = PhotoList.CLOSED_AVATAR
        elif self.type == "WAL":
            self.type = PhotoList.CLOSED_WALL
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPhotoListPosition
            CommunityPhotoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserPhotoListPosition
            UserPhotoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = PhotoList.LIST
        elif self.type == "_CLOM":
            self.type = PhotoList.MAIN
        elif self.type == "_CLOM":
            self.type = PhotoList.MANAGER
        elif self.type == "_CLOW":
            self.type = PhotoList.WALL
        elif self.type == "_CLOA":
            self.type = PhotoList.AVATAR
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPhotoListPosition
            CommunityPhotoListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserPhotoListPosition
            UserPhotoListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHL", object_id=self.pk, verb="ITE").update(status="R")


class Photo(models.Model):
    PUBLISHED, MANAGER, DELETED, CLOSED, MESSAGE = 'PUB','MAN','_DEL','_CLO','_MES'
    DELETED_MANAGER, CLOSED_MANAGER = '_DELM','_CLOM'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),(MESSAGE, 'Загруженный в сообщениях'),
        (DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    list = models.ForeignKey(PhotoList, on_delete=models.SET_NULL, related_name='photo_list', blank=True, null=True)
    file = ProcessedImageField(format='JPEG', options={'quality': 100}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=1024, upscale=False)])
    preview = ProcessedImageField(format='JPEG', options={'quality': 60}, upload_to=upload_to_photo_directory, processors=[Transpose(), ResizeToFit(width=102, upscale=False)])
    description = models.TextField(max_length=250, blank=True, null=True, verbose_name="Описание")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создано")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='photo_creator', null=False, blank=False, verbose_name="Создатель")
    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    type = models.CharField(choices=TYPE, max_length=5)
    community = models.ForeignKey('communities.Community', related_name='photo_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")
    order = models.PositiveIntegerField(default=0)
    is_photo = models.BooleanField(default=True)

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ["-order"]

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def count_reposts(self):
        if self.repost == 0:
            return ''
        else:
            return self.repost

    def get_preview(self):
        if self.preview:
            return self.preview.url
        else:
            return '/static/images/no_img/list.jpg'

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

    @classmethod
    def create_photo(cls, creator, image, list, type, community=None):
        from common.processing.photo import get_photo_processing

        list.count += 1
        list.save(update_fields=["count"])
        photo = cls.objects.create(creator=creator,list=list, order=list.count,preview=image,file=image,community=community)

        get_photo_processing(photo, Photo.PUBLISHED)
        if community:
            community.plus_photos(1)
            community_id = community.pk
        else:
            creator.plus_photos(1)
        return photo

    def is_list_exists(self):
        return self.photo_list.filter(creator=self.creator).exists()

    def get_comments(self):
        return PhotoComment.objects.filter(item_id=self.pk, parent__isnull=True)

    def count_comments(self):
        if self.comment > 0:
            return self.comment
        else:
            return ''

    def is_avatar(self, user):
        try:
            avatar = user.get_avatar_photos().order_by('-id')[0]
            return avatar == self
        except:
            return None

    def likes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__lt=0)

    def likes_count(self):
        if self.like > 0:
            return self.like
        else:
            return ''

    def reposts_count(self):
        if self.repost > 0:
            return self.repost
        else:
            return ''

    def window_likes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__gt=0)[0:6]

    def dislikes_count(self):
        if self.dislike > 0:
            return self.dislike
        else:
            return ''

    def window_dislikes(self):
        from common.model.votes import PhotoVotes
        return PhotoVotes.objects.filter(parent_id=self.pk, vote__lt=0)[0:6]

    def get_type(self):
        return self.list.all()[0].type

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Photo.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Photo.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Photo.DELETED
        elif self.type == "MAN":
            self.type = Photo.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_photos(1)
        else:
            self.creator.minus_photos(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Photo.PUBLISHED
        elif self.type == "_DELM":
            self.type = Photo.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_photos(1)
        else:
            self.creator.plus_photos(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Photo.CLOSED
        elif self.type == "MAN":
            self.type = Photo.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_photos(1)
        else:
            self.creator.minus_photos(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Photo.PUBLISHED
        elif self.type == "_CLOM":
            self.type = Photo.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_photos(1)
        else:
            self.creator.plus_photos(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="PHO", object_id=self.pk, verb="ITE").update(status="R")

    def send_like(self, user, community):
        import json
        from common.model.votes import PhotoVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PhotoVotes.objects.get(parent=self, user=user)
            if item.vote != PhotoVotes.LIKE:
                item.vote = PhotoVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=self, user=user, vote=PhotoVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "PHO", "u_photo_notify", "LIK")
                community_wall(user, community, None, self.pk, "PHO", "u_photo_notify", "LIK")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "PHO", "u_photo_notify", "LIK")
                user_wall(user, None, self.pk, "PHO", "u_photo_notify", "LIK")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PhotoVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PhotoVotes.objects.get(parent=self, user=user)
            if item.vote != PhotoVotes.DISLIKE:
                item.vote = PhotoVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PhotoVotes.DoesNotExist:
            PhotoVotes.objects.create(parent=self, user=user, vote=PhotoVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "PHO", "u_photo_notify", "DIS")
                community_wall(user, community, None, self.pk, "PHO", "u_photo_notify", "DIS")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "PHO", "u_photo_notify", "DIS")
                user_wall(user, None, self.pk, "PHO", "u_photo_notify", "DIS")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_suspended(self):
        return False


class PhotoComment(models.Model):
    EDITED, PUBLISHED, DRAFT = 'EDI', 'PUB', '_DRA'
    DELETED, EDITED_DELETED = '_DEL', '_DELE'
    CLOSED, EDITED_CLOSED = '_CLO', '_CLOE'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(DRAFT, 'Черновик'),
        (DELETED, 'Удалённый'), (EDITED_DELETED, 'Удалённый изменённый'),
        (CLOSED, 'Закрытый менеджером'), (EDITED_CLOSED, 'Закрытый изменённый'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='photo_comment_replies', null=True, blank=True,verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True,null=True)
    item = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип альбома")
    sticker = models.ForeignKey(Stickers, blank=True, null=True, on_delete=models.CASCADE, related_name="+")

    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']), )
        verbose_name="комментарий к записи"
        verbose_name_plural="комментарии к записи"

    def __str__(self):
        return "{0}/{1}".format(self.commenter.get_full_name(), self.text[:10])

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return PhotoComment.objects.filter(parent=self).all()

    def count_replies(self):
        return self.photo_comment_replies.filter(Q(type=PhotoComment.EDITED)|Q(type=PhotoComment.PUBLISHED)).values("pk").count()

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

    def likes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)

    def window_likes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__gt=0)[0:6]

    def dislikes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)

    def window_dislikes(self):
        from common.model.votes import PhotoCommentVotes
        return PhotoCommentVotes.objects.filter(item_id=self.pk, vote__lt=0)[0:6]

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

    def reposts_count(self):
        if self.repost > 0:
            return self.repost
        else:
            return ''

    @classmethod
    def create_comment(cls, commenter, attach, item, parent, text, community, sticker):
        from common.notify.notify import community_wall, community_notify, user_wall, user_notify
        from common.processing_2 import get_text_processing

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        _text = get_text_processing(text)
        item.comment += 1
        item.save(update_fields=["comment"])
        if sticker:
            comment = PhotoComment.objects.create(commenter=commenter, sticker_id=sticker, parent=parent, item=item)
        else:
            comment = PhotoComment.objects.create(commenter=commenter, attach=_attach, parent=parent, item=item, text=_text)
        if comment.parent:
            if community:
                community_notify(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
                community_wall(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
            else:
                user_notify(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
                user_wall(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "REP")
        else:
            if comment.item.community:
                community_notify(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
                community_wall(comment.commenter, community, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
            else:
                user_notify(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
                user_wall(comment.commenter, None, comment.pk, "PHOC", "u_photo_comment_notify", "COM")
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
        self.type = PhotoComment.EDITED
        self.save()
        return self

    def get_attach(self, user):
        from common.attach.comment_attach import get_comment_attach
        return get_comment_attach(self, user)

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = PhotoComment.DELETED
        elif self.type == "EDI":
            self.type = PhotoComment.EDITED_DELETED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.photo.comment -= 1
            self.parent.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.photo.comment -= 1
            self.photo.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = PhotoComment.PUBLISHED
        elif self.type == "_DELE":
            self.type = PhotoComment.EDITED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.item.comment += 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.item.comment += 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = PhotoComment.CLOSED
        elif self.type == "EDI":
            self.type = PhotoComment.EDITED_CLOSED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.item.comment -= 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.item.comment -= 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = PhotoComment.PUBLISHED
        elif self.type == "_CLOE":
            self.type = PhotoComment.EDITED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.item.comment += 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.item.comment += 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="PHOC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="PHOC", object_id=self.pk, verb="COM").update(status="R")

    def send_like(self, user, community):
        import json
        from common.model.votes import PhotoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PhotoCommentVotes.objects.get(item=self, user=user)
            if item.vote != PhotoCommentVotes.LIKE:
                item.vote = PhotoCommentVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=self, user=user, vote=PhotoCommentVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LRE")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LRE")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "LCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PhotoCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PhotoCommentVotes.objects.get(item=self, user=user)
            if item.vote != PhotoCommentVotes.DISLIKE:
                item.vote = PhotoCommentVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PhotoCommentVotes.DoesNotExist:
            PhotoCommentVotes.objects.create(item=self, user=user, vote=PhotoCommentVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DRE")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DRE")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                    community_wall(user, community, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
                    user_wall(user, None, self.pk, "PHOC", "u_photo_comment_notify", "DCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    def get_format_text(self):
        from common.utils import hide_text
        return hide_text(self.text)

    def get_edit_attach(self, user):
        from common.attach.comment_attach import get_comment_edit
        return get_comment_edit(self, user)

    def get_item(self):
        if self.parent:
            return self.parent.item
        else:
            return self.item


class PhotoListPerm(models.Model):
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

    list = models.ForeignKey(PhotoList, related_name='+', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Список записей")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=False, verbose_name="Пользователь")

    can_see_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит список/фотографии")
    can_see_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комментарии")
    create_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает фотографии")
    create_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комментарии")
    can_copy = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто может добавлять список/фотографии себе")

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

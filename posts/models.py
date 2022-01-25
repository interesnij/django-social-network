import uuid
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.contrib.postgres.indexes import BrinIndex
from common.utils import try_except
from common.model.other import Stickers


class PostsList(models.Model):
    MAIN, LIST, MANAGER, DRAFT, TEST = 'MAI','LIS','MAN','_DRA','_T'
    DELETED, DELETED_MANAGER = '_DEL','_DELM'
    CLOSED, CLOSED_MAIN, CLOSED_MANAGER = '_CLO','_CLOM','_CLOMA'

    ALL_CAN,FRIENDS,EACH_OTHER,FRIENDS_BUT,SOME_FRIENDS,MEMBERS,CREATOR,ADMINS,MEMBERS_BUT,SOME_MEMBERS = 1,2,3,4,5,6,7,8,9,10
    TYPE = (
        (MAIN, 'Основной'),(TEST, 'TEST'),(LIST, 'Пользовательский'),(MANAGER, 'Созданный персоналом'),(DRAFT, 'Предложка'),
        (DELETED, 'Удалённый'),(DELETED_MANAGER, 'Удалённый менеджерский'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_MAIN, 'Закрытый основной'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    PERM = (
            (ALL_CAN, 'Все пользователи'),
            (FRIENDS, 'Друзья'),
            (EACH_OTHER, 'Друзья и друзья друзей'),
            (CREATOR, 'Только я'),
            (FRIENDS_BUT, 'Друзья, кроме'),
            (SOME_FRIENDS, 'Некоторые друзья'),
            (MEMBERS, 'Подписчики'),
            (ADMINS, 'Администраторы'),
            (MEMBERS_BUT, 'Подписчики, кроме'),
            (SOME_MEMBERS, 'Некоторые подписчики'),
            )

    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_postslist', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_postslist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип списка")
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
    is_post_list = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " - " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список записей"
        verbose_name_plural = "списки записей"

    def count_items_ru(self):
        count = self.count_items()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " запись"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " записи"
        else:
            return str(count) + " записей"

    def get_can_see_el_exclude_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_include_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_exclude_users_ids())
    def get_can_see_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_include_users_ids())

    def get_can_see_comment_exclude_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_comment_include_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_comment_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_comment_exclude_users_ids())
    def get_can_see_comment_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_comment_include_users_ids())

    def get_create_el_exclude_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_include_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_exclude_users_ids())
    def get_create_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_include_users_ids())

    def get_create_comment_exclude_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_comment_include_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_comment_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_comment_exclude_users_ids())
    def get_create_comment_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_comment_include_users_ids())

    def get_copy_el_exclude_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_include_users_ids(self):
        list = PostsListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_copy_el_exclude_users_ids())
    def get_copy_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_copy_el_include_users_ids())

    @classmethod
    def create_list(cls,creator,name,description,community,can_see_el,can_see_comment,create_el,create_comment,copy_el,\
        can_see_el_users,can_see_comment_users,create_el_users,create_comment_users,copy_el_users):
        from common.processing.post import get_post_list_processing

        list = cls.objects.create(creator=creator,name=name,description=description,community=community,can_see_el=can_see_el,can_see_comment=can_see_comment,create_el=create_el,create_comment=create_comment,copy_el=copy_el)
        if community:
            from communities.model.list import CommunityPostsListPosition

            CommunityPostsListPosition.objects.create(community=community.pk, list=list.pk, position=PostsList.get_community_lists_count(community.pk))
        else:
            from users.model.list import UserPostsListPosition
            UserPostsListPosition.objects.create(user=creator.pk, list=list.pk, position=PostsList.get_user_lists_count(creator.pk))

        get_post_list_processing(list, PostsList.LIST)

        if can_see_el == 4 or can_see_el == 9:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])

        if can_see_comment == 4 or can_see_comment == 9:
            if can_see_comment_users:
                for user_id in can_see_comment_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_comment = 2
                    perm.save(update_fields=["can_see_comment"])
            else:
                list.can_see_comment = 7
                list.save(update_fields=["can_see_comment"])
        elif can_see_comment == 5 or can_see_comment == 10:
            if can_see_comment_users:
                for user_id in can_see_comment_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_comment = 1
                    perm.save(update_fields=["can_see_comment"])
            else:
                list.can_see_comment = 7
                list.save(update_fields=["can_see_comment"])

        if create_el == 4 or create_el == 9:
            if create_el_users:
                for user_id in create_el_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                for user_id in create_el_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])

        if create_comment == 4 or create_comment == 9:
            if create_comment_users:
                for user_id in create_comment_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_comment = 2
                    perm.save(update_fields=["create_comment"])
            else:
                list.create_comment = 7
                list.save(update_fields=["create_comment"])
        elif create_comment == 5 or create_comment == 10:
            if create_comment_users:
                for user_id in create_comment_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_comment = 1
                    perm.save(update_fields=["create_comment"])
            else:
                list.create_comment = 7
                list.save(update_fields=["create_comment"])

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                list.copy_el = 7
                list.save(update_fields=["copy_el"])
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = PostsListPerm.get_or_create_perm(list.pk, user_id)
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
                PostsListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7

        if can_see_comment == 4 or can_see_comment == 9:
            if can_see_comment_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(can_see_comment=0)
                for user_id in can_see_comment_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_comment = 2
                    perm.save(update_fields=["can_see_comment"])
            else:
                self.can_see_comment = 7
        elif can_see_comment == 5 or can_see_comment == 10:
            if can_see_comment_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(can_see_comment=0)
                for user_id in can_see_comment_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_comment = 1
                    perm.save(update_fields=["can_see_comment"])
            else:
                self.can_see_comment = 7

        if create_el == 4 or create_el == 9:
            if create_el_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7

        if create_comment == 4 or create_comment == 9:
            if create_comment_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(create_comment=0)
                for user_id in create_comment_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_comment = 2
                    perm.save(update_fields=["create_comment"])
            else:
                self.create_comment = 7
        elif create_comment == 5 or create_comment == 10:
            if create_comment_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(create_comment=0)
                for user_id in create_comment_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_comment = 1
                    perm.save(update_fields=["create_comment"])
            else:
                self.create_comment = 7

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                PostsListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = PostsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 1
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7

        self.save()
        return self

    def is_suspended(self):
        return False

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
            community = self.community
            if self.create_el == self.ALL_CAN:
                return True
            elif self.create_el == self.CREATOR and user_id == community.creator.pk:
                return True
            elif self.create_el == self.ADMINS and user_id in community.get_admins_ids():
                return True
            elif self.create_el == self.MEMBERS and user_id in community.get_members_ids():
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

    def get_order(self):
        from users.model.list import UserPostsListPosition
        return UserPostsListPosition.objects.get(list=self.pk)

    def add_in_community_collections(self, community):
        from communities.model.list import CommunityPostsListPosition
        CommunityPostsListPosition.objects.create(community=community.pk, list=self.pk, position=PostsList.get_community_lists_count(community.pk))
        self.communities.add(community)
    def remove_in_community_collections(self, community):
        from communities.model.list import CommunityPostsListPosition
        CommunityPostsListPosition.objects.get(community=community.pk, list=self.pk).delete()
        self.communities.remove(user)
    def add_in_user_collections(self, user):
        from users.model.list import UserPostsListPosition
        UserPostsListPosition.objects.create(user=user.pk, list=self.pk, position=PostsList.get_user_lists_count(user.pk))
        self.users.add(user)
    def remove_in_user_collections(self, user):
        from users.model.list import UserPostsListPosition
        UserPostsListPosition.objects.get(user=user.pk, list=self.pk).delete()
        self.users.remove(user)

    def is_item_in_list(self, item_id):
        return self.post_list.filter(pk=item_id).values("pk").exists()

    def get_items(self):
        return self.post_list.select_related('creator').only('creator__id', 'created').filter(list=self,type="PUB")
    def get_manager_items(self):
        return self.post_list.filter(type="MAN")
    def count_items(self):
        return self.post_list.filter(type="PUB").values("pk").count()

    def is_not_empty(self):
        return self.post_list.filter(type="PUB").values("pk").exists()

    def get_posts_ids(self):
        ids = self.post_list.filter(type="FIX").values("pk")
        return [id['pk'] for id in ids]

    def is_user_can_add_list(self, user_id):
        return self.creator.pk != user_id and user_id not in self.get_users_ids()

    def is_user_can_delete_list(self, user_id):
        return self.creator.pk != user_id and user_id in self.get_users_ids()

    def is_community_can_add_list(self, community_id):
        return self.community.pk != community_id and community_id not in self.get_communities_ids()

    def is_community_can_delete_list(self, community_id):
        return self.community.pk != community_id and community_id in self.get_communities_ids()

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]

    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in communities]

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_open(self):
        return self.type[0] == "_"
    def is_have_edit(self):
        return self.is_list()
    def is_have_get(self):
        return self.is_list() or self.is_main()

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        try:
            from users.model.list import UserPostsListPosition
            query = []
            lists = UserPostsListPosition.objects.filter(user=user_pk).values("list")
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
            from users.model.list import UserPostsListPosition
            query = []
            lists = UserPostsListPosition.objects.filter(user=user_pk).values("list")
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
            from communities.model.list import CommunityPostsListPosition
            query = []
            lists = CommunityPostsListPosition.objects.filter(community=community_pk).values("list")
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
            from communities.model.list import CommunityPostsListPosition
            query = []
            lists = CommunityPostsListPosition.objects.filter(community=community_pk).values("list")
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

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = PostsList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = PostsList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self):
        from notify.models import Notify, Wall

        if self.type == "LIS":
            self.type = PostsList.DELETED
        elif self.type == "MAN":
            self.type = PostsList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPostsListPosition
            CommunityPostsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserPostsListPosition
            UserPostsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = PostsList.LIST
        elif self.type == "_DELM":
            self.type = PostsList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPostsListPosition
            CommunityPostsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserPostsListPosition
            UserPostsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = PostsList.CLOSED
        elif self.type == "MAI":
            self.type = PostsList.CLOSED_MAIN
        elif self.type == "MAN":
            self.type = PostsList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPostsListPosition
            CommunityPostsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserPostsListPosition
            UserPostsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = PostsList.LIST
        elif self.type == "_CLOM":
            self.type = PostsList.MAIN
        elif self.type == "_CLOM":
            self.type = PostsList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPostsListPosition
            CommunityPostsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserPostsListPosition
            UserPostsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POL", object_id=self.pk, verb="ITE").update(status="R")

    def get_user_creator_draft_post(self, user_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, type=Post.CREATOR_DRAFT).first()
    def is_user_have_creator_draft_post(self, user_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, type=Post.CREATOR_DRAFT).exists()
    def get_user_offer_draft_post(self, user_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, type=Post.OFFER_DRAFT).first()
    def is_user_have_offer_draft_post(self, user_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, type=Post.OFFER_DRAFT).exists()

    def get_community_creator_draft_post(self, user_id, community_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, community_id=community_id, type=Post.CREATOR_DRAFT).first()
    def is_community_have_creator_draft_post(self, user_id, community_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, community_id=community_id, type=Post.CREATOR_DRAFT).exists()
    def get_user_offer_draft_post(self, user_id, community_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, community_id=community_id, type=Post.OFFER_DRAFT).first()
    def is_user_have_offer_draft_post(self, user_id, community_id):
        return Post.objects.filter(list_id=self.pk, creator_id=user_id, community_id=community_id, type=Post.OFFER_DRAFT).exists()


class PostCategory(models.Model):
	name = models.CharField(max_length=100, verbose_name="Тематика")
	order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Тематика постов"
		verbose_name_plural = "Тематики постов"


class Post(models.Model):
    C_OFFER, U_OFFER, CREATOR_DRAFT, OFFER_DRAFT, FIXED, PUBLISHED, MANAGER, DELETED, CLOSED, REPOST = "_COF","_UOF","_CDR","_COF","FIX",'PUB','MAN','_DEL','_CLO','_REP'
    DELETED_C_OFFER, DELETED_U_OFFER, DELETED_MANAGER, CLOSED_MANAGER = '_DCOF','_DUOF','_DELM','_CLOM'
    TYPE = (
        (C_OFFER, 'Предложка сообщества'),(U_OFFER, 'Предложка пользователя'),(CREATOR_DRAFT, 'Черновик владельца'),(OFFER_DRAFT, 'Черновик предложки'),(FIXED, 'Закреплен'), (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_C_OFFER, 'Удалённая предложка сообщества'),(DELETED_MANAGER, 'Удалённая предложка пользователя'),(DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_MANAGER, 'Закрытый менеджерский'),(REPOST, 'Репост'),
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='post_creator', on_delete=models.SET_NULL, verbose_name="Создатель")
    category = models.ForeignKey(PostCategory, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="Тематика")
    list = models.ForeignKey(PostsList, blank=True, null=True, on_delete=models.SET_NULL, related_name='post_list')
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL, related_name="thread")
    community = models.ForeignKey('communities.Community', related_name='post_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    type = models.CharField(choices=TYPE, max_length=5, verbose_name="Статус статьи")
    text = models.TextField(max_length=settings.POST_MAX_LENGTH, blank=True, verbose_name="Текст")

    comments_enabled = models.BooleanField(default=True, verbose_name="Разрешить комментарии")
    is_signature = models.BooleanField(default=True, verbose_name="Подпись автора")
    votes_on = models.BooleanField(default=True, verbose_name="Реакции разрешены")
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")

    comment = models.PositiveIntegerField(default=0, verbose_name="Кол-во комментов")
    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    ad_view = models.PositiveIntegerField(default=0, verbose_name="Кол-во рекламных просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")
    order = models.PositiveIntegerField(default=0)
    is_post = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-order"]

    def __str__(self):
        return self.creator.get_full_name()

    def get_format_text(self):
        from common.utils import hide_text
        return hide_text(self.text)

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
    def plus_ad_views(self, count):
        self.ad_view += count
        return self.save(update_fields=['ad_view'])
    def plus_reposts(self, count):
        self.repost += count
        return self.save(update_fields=['repost'])
    def minus_reposts(self, count):
        self.repost -= count
        return self.save(update_fields=['repost'])

    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_fixed(self):
        return self.type == "FIXED"
    def is_suspended(self):
        return False
    def is_repost(self):
        """ это все репосты, которые содержат все, кроме репостов постов """
        return self.type == self.REPOST

    def send_like(self, user, community):
        import json
        from common.model.votes import PostVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PostVotes.objects.get(parent=self, user=user)
            if item.vote != PostVotes.LIKE:
                item.vote = PostVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=self, user=user, vote=PostVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "POS", "u_post_notify", "LIK")
                community_wall(user, community, None, self.pk, "POS", "u_post_notify", "LIK")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "POS", "u_post_notify", "LIK")
                user_wall(user, None, self.pk, "POS", "u_post_notify", "LIK")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PostVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        if not self.votes_on:
            from django.http import Http404
            raise Http404
        try:
            item = PostVotes.objects.get(parent=self, user=user)
            if item.vote != PostVotes.DISLIKE:
                item.vote = PostVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PostVotes.DoesNotExist:
            PostVotes.objects.create(parent=self, user=user, vote=PostVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(user, community, None, self.pk, "POS", "u_post_notify", "DIS")
                community_wall(user, community, None, self.pk, "POS", "u_post_notify", "DIS")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(user, None, self.pk, "POS", "u_post_notify", "DIS")
                user_wall(user, None, self.pk, "POS", "u_post_notify", "DIS")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    @classmethod
    def create_post(cls, creator, text, category, list, attach, parent, comments_enabled, is_signature, votes_on, community=None, type=None):
        from common.processing_2 import get_text_processing
        from rest_framework.exceptions import PermissionDenied

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

        _text = get_text_processing(text)

        list.count += 1
        if type:
            _type = type
        else:
            _type = "PUB"
        list.save(update_fields=["count"])
        post = cls.objects.create(creator=creator,list=list,order=list.count,text=_text,category=category,parent=parent,community=community,comments_enabled=comments_enabled,is_signature=is_signature,votes_on=votes_on,attach=_attach,type=_type)
        return post

    @classmethod
    def create_offer_post(cls, creator, text, list, attach, community):
        from common.processing_2 import get_text_processing
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

        _text = get_text_processing(text)
        post = cls.objects.create(creator=creator,list=list,text=_text,community=community,attach=_attach,type=Post.C_OFFER)
        return post

    @classmethod
    def create_creator_draft_post(cls, creator, text, category, list, attach, parent, comments_enabled, is_signature, votes_on, community):
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

        if community:
            if list.is_community_have_creator_draft_post(creator.pk, community.pk):
                post = list.get_community_creator_draft_post(creator.pk, community.pk)
                post.text = text
                post.community = community
                post.category = category
                post.attach = _attach
                post.parent = parent
                post.comments_enabled = comments_enabled
                post.is_signature = is_signature
                post.votes_on = votes_on
                post.save()
            else:
                post = cls.objects.create(creator=creator,list=list,text=text,category=category,parent=parent,community=community,comments_enabled=comments_enabled,is_signature=is_signature,votes_on=votes_on,attach=_attach)
        else:
            if list.is_user_have_creator_draft_post(creator.pk):
                post = list.get_user_creator_draft_post(creator.pk)
                post.text = text
                post.category = category
                post.attach = _attach
                post.parent = parent
                post.comments_enabled = comments_enabled
                post.votes_on = votes_on
                post.save()
            else:
                post = cls.objects.create(creator=creator,list=list,text=text,category=category,parent=parent,comments_enabled=comments_enabled,votes_on=votes_on,attach=_attach)
        return post

    @classmethod
    def create_offer_draft_post(cls, creator, text, category, list, attach, parent, comments_enabled, is_signature, votes_on, community):
        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

        if community:
            if list.is_community_have_offer_draft_post(creator.pk, community.pk):
                post = list.get_community_offer_draft_post(creator.pk, community.pk)
                post.text = text
                post.community = community
                post.category = category
                post.attach = _attach
                post.parent = parent
                post.comments_enabled = comments_enabled
                post.is_signature = is_signature
                post.votes_on = votes_on
                post.save()
            else:
                post = cls.objects.create(creator=creator,list=list,text=text,category=category,parent=parent,community=community,comments_enabled=comments_enabled,is_signature=is_signature,votes_on=votes_on,attach=_attach)
        else:
            if list.is_user_have_offer_draft_post(creator.pk):
                post = list.get_user_offer_draft_post(creator.pk)
                post.text = text
                post.category = category
                post.attach = _attach
                post.parent = parent
                post.comments_enabled = comments_enabled
                post.votes_on = votes_on
                post.save()
            else:
                post = cls.objects.create(creator=creator,list=list,text=text,category=category,parent=parent,comments_enabled=comments_enabled,votes_on=votes_on,attach=_attach)
        return post

    def edit_post(self, text, list, category, attach, comments_enabled, is_signature, votes_on):
        from common.processing_2 import get_text_processing

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        _text = get_text_processing(text)

        if self.list.pk != list:
            self.list.count -= 1
            self.list.save(update_fields=["count"])
            list.count += 1
            list.save(update_fields=["count"])
        self.text = _text
        self.category = category
        self.attach = _attach
        self.comments_enabled = comments_enabled
        self.is_signature = is_signature
        self.list = list
        self.votes_on = votes_on
        self.save()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Post.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Post.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Post.DELETED
        elif self.type == "MAN":
            self.type = Post.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_posts(1)
        else:
            self.creator.minus_posts(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Post.PUBLISHED
        elif self.type == "_DELM":
            self.type = Post.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_posts(1)
        else:
            self.creator.plus_posts(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, comunity):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Post.CLOSED
        elif self.type == "MAN":
            self.type = Post.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_posts(1)
        else:
            self.creator.minus_posts(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Post.PUBLISHED
        elif self.type == "_CLOM":
            self.type = Post.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_posts(1)
        else:
            self.creator.plus_posts(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="POS", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def create_parent_post(cls, creator, community, attach):
        post = cls.objects.create(creator=creator, community=community, attach=attach, type=Post.REPOST)
        return post

    def get_u_new_parent(self, user):
        from common.attach.post_attach import get_u_news_parent
        return get_u_news_parent(self.parent, user)

    def get_c_new_parent(self, user):
        from common.attach.post_attach import get_c_news_parent
        return get_c_news_parent(self.parent, user)

    def get_u_post_parent(self, user):
        from common.attach.post_attach import get_u_posts_parent
        return get_u_posts_parent(self.parent, user)

    def get_c_post_parent(self, user):
        from common.attach.post_attach import get_c_posts_parent
        return get_c_posts_parent(self.parent, user)

    def get_attach(self, user):
        from common.attach.post_elements import get_post_attach
        return get_post_attach(self, user)

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def count_comments(self):
        if self.comment == 0:
            return ''
        else:
            return self.comment

    def get_comments(self):
        return PostComment.objects.filter(item_id=self.pk, parent__isnull=True).exclude(type__contains="_")

    def fixed_post(self, obj):
        if obj.is_can_fixed_post():
            self.type = Post.FIXED
            return self.save(update_fields=["type"])
        else:
            return ValidationError("Список уже заполнен.")

    def unfixed_post(self):
        if self.is_fixed:
            self.type = Post.PUBLISHED
            return self.save(update_fields=["type"])
        else:
            self.type = Post.FIXED
            self.save(update_fields=["type"])

    def likes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__lt=0)

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

    def likes_count_ru(self):
        count = self.likes_count()
        if not count:
            return '<span data-count="like">' + str(0) + '</span> просмотров'
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            i = " просмотр"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            i = " просмотра"
        else:
            i = " просмотров"
        return '<span data-count="like">' + str(count) + '</span>' + i
    def dislikes_count_ru(self):
        count = self.dislikes_count()
        if not count:
            return '<span data-count="dislike">' + str(0) + '</span> просмотров'
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            i = " просмотр"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            i = " просмотра"
        else:
            i = " просмотров"
        return '<span data-count="dislike">' + str(count) + '</span>' + i

    def window_likes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__gt=0)[0:6]
    def is_have_likes(self):
        return self.like > 0
    def window_dislikes(self):
        from common.model.votes import PostVotes
        return PostVotes.objects.filter(parent_id=self.pk, vote__lt=0)[0:6]
    def is_have_dislikes(self):
        return self.dislike > 0

    def get_reposts(self):
        return Post.objects.filter(parent=self)

    def get_window_reposts(self):
        return Post.objects.filter(parent=self)[0:6]

    def count_reposts(self):
        if self.repost == 0:
            return ''
        else:
            return self.repost

    def get_visiter_sity(self):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        return UserLocation.objects.filter(user_id__in=ids).distinct('city_ru')

    def get_sity_count(self, sity):
        from stst.models import PostNumbers, PostAdNumbers
        from users.model.profile import UserLocation

        posts = PostNumbers.objects.filter(post=self.pk).values('user')
        ads_posts = PostAdNumbers.objects.filter(post=self.pk).values('user')
        user_ids = posts + ads_posts
        ids = [use['user'] for use in user_ids]
        return UserLocation.objects.filter(user_id__in=ids, city_ru=sity).values('pk').count()

    def all_visits_count(self):
        count = self.visits_count() + self.ad_visits_count()
        if count == 0:
            return ''
        else:
            return count

    def get_list_pk(self):
        return self.list.pk

    def visits_count(self):
        return self.view
    def ad_visits_count(self):
        return self.ad_view

    def get_attach_photos(self):
        if "pho" in self.attach:
            query = []
            from gallery.models import Photo

            for item in self.attach.split(","):
                if item[:3] == "pho":
                    query.append(item[3:])
        return Photo.objects.filter(id__in=query)

    def get_attach_videos(self):
        if "vid" in self.attach:
            query = []
            from video.models import Video

            for item in self.attach.split(","):
                if item[:3] == "vid":
                    query.append(item[3:])
        return Video.objects.filter(id__in=query)
    def is_private(self):
        return self.type == self.PRIVATE

    def get_edit_attach(self, user):
        from common.attach.post_elements import get_post_edit
        return get_post_edit(self, user)

    def get_count_attach(self):
        if self.attach:
            length = self.attach.split(",")
            return "files_" + str(len(length))
        else:
            return "files_0"


class PostComment(models.Model):
    EDITED, PUBLISHED, DRAFT = 'EDI', 'PUB', '_DRA'
    DELETED, EDITED_DELETED = '_DEL', '_DELE'
    CLOSED, EDITED_CLOSED = '_CLO', '_CLOE'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(EDITED, 'Изменённый'),(DRAFT, 'Черновик'),
        (DELETED, 'Удалённый'), (EDITED_DELETED, 'Удалённый изменённый'),
        (CLOSED, 'Закрытый менеджером'), (EDITED_CLOSED, 'Закрытый изменённый'),
    )
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, verbose_name="Родительский комментарий")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    commenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Комментатор")
    text = models.TextField(blank=True)
    item = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    attach = models.CharField(blank=True, max_length=200, verbose_name="Прикрепленные элементы")
    type = models.CharField(max_length=5, choices=TYPE, verbose_name="Тип альбома")
    sticker = models.ForeignKey(Stickers, blank=True, null=True, on_delete=models.CASCADE, related_name="+")

    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = "комментарий к записи"
        verbose_name_plural = "комментарии к записи"

    def __str__(self):
        return self.commenter.get_full_name()

    def send_like(self, user, community):
        import json
        from common.model.votes import PostCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PostCommentVotes.objects.get(item=self, user=user)
            if item.vote != PostCommentVotes.LIKE:
                item.vote = PostCommentVotes.LIKE
                item.save(update_fields=['vote'])
                self.like += 1
                self.dislike -= 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.like -= 1
                self.save(update_fields=['like'])
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=self, user=user, vote=PostCommentVotes.LIKE)
            self.like += 1
            self.save(update_fields=['like'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LRE")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_notify", "LRE")
                    user_wall(user, None, self.pk, "POSC", "u_post_notify", "LCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
                    user_wall(user, None, self.pk, "POSC", "u_post_comment_notify", "LCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")
    def send_dislike(self, user, community):
        import json
        from common.model.votes import PostCommentVotes
        from django.http import HttpResponse
        from common.notify.notify import user_notify, user_wall
        try:
            item = PostCommentVotes.objects.get(item=self, user=user)
            if item.vote != PostCommentVotes.DISLIKE:
                item.vote = PostCommentVotes.DISLIKE
                item.save(update_fields=['vote'])
                self.like -= 1
                self.dislike += 1
                self.save(update_fields=['like', 'dislike'])
            else:
                item.delete()
                self.dislike -= 1
                self.save(update_fields=['dislike'])
        except PostCommentVotes.DoesNotExist:
            PostCommentVotes.objects.create(item=self, user=user, vote=PostCommentVotes.DISLIKE)
            self.dislike += 1
            self.save(update_fields=['dislike'])
            if self.parent:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DRE")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_comment_notify", "DRE")
                    user_wall(user, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
            else:
                if community:
                    from common.notify.notify import community_notify, community_wall
                    community_notify(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                    community_wall(user, community, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                else:
                    from common.notify.notify import user_notify, user_wall
                    user_notify(user, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
                    user_wall(user, None, self.pk, "POSC", "u_post_comment_notify", "DCO")
        return HttpResponse(json.dumps({"like_count": str(self.likes_count()),"dislike_count": str(self.dislikes_count())}),content_type="application/json")

    def get_created(self):
        from django.contrib.humanize.templatetags.humanize import naturaltime
        return naturaltime(self.created)

    def get_replies(self):
        return self.replies.filter(~Q(type__contains="_")).only("pk")

    def count_replies(self):
        return self.replies.filter(Q(type=PostComment.EDITED)|Q(type=PostComment.PUBLISHED)).values("pk").count()

    def likes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__gt=0)

    def dislikes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__lt=0)

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

    def window_likes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__gt=0)[0:6]

    def window_dislikes(self):
        from common.model.votes import PostCommentVotes
        return PostCommentVotes.objects.filter(item=self, vote__lt=0)[0:6]

    def __str__(self):
        return self.commenter.get_full_name()

    @classmethod
    def create_comment(cls, commenter, attach, item, parent, text, community, sticker):
        from common.processing_2 import get_text_processing

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")

        if sticker:
            comment = PostComment.objects.create(commenter=commenter, sticker_id=sticker, parent=parent, item=item)
        else:
            comment = PostComment.objects.create(commenter=commenter, attach=_attach, parent=parent, item=item, text=get_text_processing(text))
        item.comment += 1
        item.save(update_fields=["comment"])
        if parent:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
                community_wall(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
                user_wall(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "REP")
        else:
            if community:
                from common.notify.notify import community_notify, community_wall
                community_notify(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
                community_wall(comment.commenter, community, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
            else:
                from common.notify.notify import user_notify, user_wall
                user_notify(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
                user_wall(comment.commenter, None, comment.pk, "POSC", "u_post_comment_notify", "COM")
        return comment

    def edit_comment(self, attach, text):
        from common.processing_2 import get_text_processing
        if not text and not attach:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Нет текста или прикрепленных элементов")

        _attach = str(attach)
        _attach = _attach.replace("'", "").replace("[", "").replace("]", "").replace(" ", "")
        self.attach = _attach
        self.text = get_text_processing(text)
        self.type = PostComment.EDITED
        self.save()
        return self

    def count_replies_ru(self):
        count = self.count_replies()
        a, b= count % 10, count % 100
        if (a == 1) and (b != 11):
            return ''.join([str(count), " ответ"])
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return ''.join([str(count), " ответа"])
        else:
            return ''.join([str(count), " ответов"])

    def get_attach(self, user):
        from common.attach.comment_attach import get_comment_attach
        return get_comment_attach(self, user)

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = PostComment.DELETED
        elif self.type == "EDI":
            self.type = PostComment.EDITED_DELETED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.item.comment -= 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.item.comment -= 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = PostComment.PUBLISHED
        elif self.type == "_DELE":
            self.type = PostComment.EDITED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.item.comment += 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.item.comment += 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = PostComment.CLOSED
        elif self.type == "EDI":
            self.type = PostComment.EDITED_CLOSED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.item.comment -= 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="C")
        else:
            self.item.comment -= 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="C")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = PostComment.PUBLISHED
        elif self.type == "_CLOE":
            self.type = PostComment.EDITED
        self.save(update_fields=['type'])
        if self.parent:
            self.parent.item.comment += 1
            self.parent.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="REP").update(status="R")
        else:
            self.item.comment += 1
            self.item.save(update_fields=["comment"])
            if Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").exists():
                Notify.objects.filter(type="POSC", object_id=self.pk, verb__contains="COM").update(status="R")
        if Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").exists():
            Wall.objects.filter(type="POSC", object_id=self.pk, verb="COM").update(status="R")

    def get_edit_attach(self, user):
        from common.attach.comment_attach import get_comment_edit
        return get_comment_edit(self, user)

    def get_count_attach(self):
        if self.attach:
            _attach = self.attach.split(",")
            if len(_attach) == 1:
                return "files_one"
            elif len(_attach) == 2:
                return "files_two"
            else:
                return "files_null"
        else:
            return "files_null"

    def get_item(self):
        if self.parent:
            return self.parent.item
        else:
            return self.item

    def get_format_text(self):
        from common.utils import hide_text
        return hide_text(self.text)


class PostsListPerm(models.Model):
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

    list = models.ForeignKey(PostsList, related_name='+', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Список записей")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=False, verbose_name="Пользователь")

    can_see_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит список/записи")
    can_see_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комментарии")
    create_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает записи")
    create_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комментарии")
    can_copy = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто может добавлять список/записи себе")

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

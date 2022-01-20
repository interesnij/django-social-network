import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from docs.helpers import upload_to_doc_directory, validate_file_extension
from django.db.models.signals import post_save
from django.dispatch import receiver
from communities.models import Community
from django.db.models import Q


class DocsList(models.Model):
    MAIN, LIST, MANAGER, DELETED, DELETED_MANAGER, CLOSED, CLOSED_MAIN, CLOSED_MANAGER = 'MAI','LIS','MAN','_DEL','_DELM','_CLO','_CLOM','_CLOMA'
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

    name = models.CharField(max_length=255)
    #community = models.ForeignKey('communities.Community', related_name='docs_lists_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='docs_lists_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип списка")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    count = models.PositiveIntegerField(default=0)

    can_see_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит документы")
    create_el = models.PositiveSmallIntegerField(choices=PERM, default=7, verbose_name="Кто создает документы и потом с этими документами работает")
    copy_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто копирует документы")

    #users = models.ManyToManyField("users.User", blank=True, related_name='+')
    #communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')
    is_doc_list = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"

    def count_items_ru(self):
        count = self.count_items()
        a = count % 10
        b = count % 100
        if (a == 1) and (b != 11):
            return str(count) + " документ"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " документа"
        else:
            return str(count) + " документов"

    def get_can_see_el_exclude_users_ids(self):
        list = DocListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_include_users_ids(self):
        list = DocListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_exclude_users_ids())
    def get_can_see_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_include_users_ids())

    def get_create_el_exclude_users_ids(self):
        list = DocListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_include_users_ids(self):
        list = DocListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_exclude_users_ids())
    def get_create_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_include_users_ids())

    def get_copy_el_exclude_users_ids(self):
        list = DocListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_include_users_ids(self):
        list = DocListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_copy_el_exclude_users_ids())
    def get_copy_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_copy_el_include_users_ids())

    def add_in_community_collections(self, community):
        from communities.model.list import CommunityDocsListPosition
        CommunityDocsListPosition.objects.create(community=community.pk, list=self.pk, position=DocsList.get_community_lists_count(community.pk))
        self.communities.add(community)
    def remove_in_community_collections(self, community):
        from communities.model.list import CommunityDocsListPosition
        CommunityDocsListPosition.objects.get(community=community.pk, list=self.pk).delete()
        self.communities.remove(user)
    def add_in_user_collections(self, user):
        from users.model.list import UserDocsListPosition
        UserDocsListPosition.objects.create(user=user.pk, list=self.pk, position=DocsList.get_user_lists_count(user.pk))
        self.users.add(user)
    def remove_in_user_collections(self, user):
        from users.model.list import UserDocsListPosition
        UserDocsListPosition.objects.get(user=user.pk, list=self.pk).delete()
        self.users.remove(user)

    def is_user_can_see_el(self, user_id):
        if self.community:
            if self.can_see_el == self.ALL_CAN:
                return True
            elif self.can_see_el == self.CREATOR and user_id == self.community.creator.pk:
                return True
            elif self.can_see_el == self.ADMINS and user_id in self.get_admins_ids():
                return True
            elif self.can_see_el == self.MEMBERS and user_id in self.community.get_admins_ids():
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

    def is_user_can_create_el(self, user_id):
        if self.community:
            if self.create_el == 1:
                return True
            elif self.create_el == 4 and user_id == self.community.creator.pk:
                return True
            elif self.create_el == self.ADMINS and user_id in self.get_admins_ids():
                return True
            elif self.create_el == self.MEMBERS and user_id in self.community.get_admins_ids():
                return True
            elif self.create_el == self.MEMBERS_BUT:
                return not user_id in self.get_create_el_exclude_users_ids()
            elif self.create_el == self.SOME_MEMBERS:
                return user_id in self.get_create_el_include_users_ids()
        else:
            if self.create_el == 1:
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

    def is_user_can_copy_el(self, user_id):
        if self.community:
            if self.copy_el == 1:
                return True
            elif self.copy_el == 4 and user_id == self.community.creator.pk:
                return True
            elif self.copy_el == self.ADMINS and user_id in self.get_admins_ids():
                return True
            elif self.copy_el == self.MEMBERS and user_id in self.community.get_admins_ids():
                return True
            elif self.copy_el == self.MEMBERS_BUT:
                return not user_id in self.get_copy_el_exclude_users_ids()
            elif self.copy_el == self.SOME_MEMBERS:
                return user_id in self.get_copy_el_include_users_ids()
        else:
            if self.copy_el == 1:
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

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            list = DocsList.objects.create(community=instance, type=DocsList.MAIN, name="Основной список", creator=instance.creator)
            from communities.model.list import CommunityDocsListPosition
            CommunityDocsListPosition.objects.create(community=instance.pk, list=list.pk, position=1)

    def is_item_in_list(self, item_id):
        return self.docs_list.filter(pk=item_id).values("pk").exists()

    def is_not_empty(self):
        return self.docs_list.exclude(type__contains="_").values("pk").exists()

    def get_items(self):
        return self.docs_list.filter(type="PUB")
    def get_manager_items(self):
        return self.docs_list.filter(type="MAN")
    def count_items(self):
        return self.docs_list.exclude(type__contains="_").values("pk").count()

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

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_open(self):
        return self.type[0] != "_"
    def is_have_edit(self):
        return self.is_list()

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        try:
            from users.model.list import UserDocsListPosition
            query = []
            lists = UserDocsListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from users.model.list import UserDocsListPosition
            query = []
            lists = UserDocsListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from communities.model.list import CommunityDocsListPosition
            query = []
            lists = CommunityDocsListPosition.objects.filter(community=community_pk, type=1).values("list")
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
            from communities.model.list import CommunityDocsListPosition
            query = []
            lists = CommunityDocsListPosition.objects.filter(community=community_pk, type=1).values("list")
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
    def create_list(cls, creator, name, description, community,can_see_el,create_el,copy_el,\
        can_see_el_users,create_el_users,copy_el_users):
        from common.processing.doc import get_doc_list_processing

        list = cls.objects.create(creator=creator,name=name,description=description,community=community,can_see_el=can_see_el,create_el=create_el,copy_el=copy_el)
        get_doc_list_processing(list, DocsList.LIST)
        if community:
            from communities.model.list import CommunityDocsListPosition
            CommunityDocsListPosition.objects.create(community=community.pk, list=list.pk, position=DocsList.get_community_lists_count(community.pk))
        else:
            from users.model.list import UserDocsListPosition
            UserDocsListPosition.objects.create(user=creator.pk, list=list.pk, position=DocsList.get_user_lists_count(creator.pk))
        if can_see_el == 4 or can_see_el == 9:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = DocsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = DocsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])

        if create_el == 4 or create_el == 9:
            if create_el_users:
                for user_id in create_el_users:
                    perm = DocsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                for user_id in create_el_users:
                    perm = DocsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = DocsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                list.copy_el = 7
                list.save(update_fields=["copy_el"])
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = DocsListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_copy = 1
                    perm.save(update_fields=["can_copy"])
            else:
                list.copy_el = 7
                list.save(update_fields=["copy_el"])
        return list
    def edit_list(self, name, description,can_see_el,create_el,copy_el,\
        can_see_el_users,create_el_users,copy_el_users):

        self.name = name
        self.description = description
        self.can_see_el = can_see_el
        self.create_el = create_el
        self.copy_el = copy_el
        if can_see_el == 4 or can_see_el == 9:
            if can_see_el_users:
                DocsListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = DocsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                DocsListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = DocsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7

        if create_el == 4 or create_el == 9:
            if create_el_users:
                DocsListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = DocsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                DocsListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = DocsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                DocsListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = DocsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                DocsListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = DocsListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 1
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7
        self.save()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = DocsList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = DocsList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocsList.DELETED
        elif self.type == "MAN":
            self.type = DocsList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityDocsListPosition
            CommunityDocsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserDocsListPosition
            UserDocsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = DocsList.LIST
        elif self.type == "_DELM":
            self.type = DocsList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityDocsListPosition
            CommunityDocsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserDocsListPosition
            UserDocsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocsList.CLOSED
        elif self.type == "MAI":
            self.type = DocsList.CLOSED_MAIN
        elif self.type == "MAN":
            self.type = DocsList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityDocsListPosition
            CommunityDocsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserDocsListPosition
            UserDocsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = DocsList.LIST
        elif self.type == "_CLOM":
            self.type = DocsList.MAIN
        elif self.type == "_CLOM":
            self.type = DocsList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityDocsListPosition
            CommunityDocsListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserDocsListPosition
            UserDocsListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")


class Doc(models.Model):
    PUBLISHED, MANAGER, DELETED, CLOSED = 'PUB','MAN','_DEL','_CLO'
    DELETED_MANAGER, CLOSED_MANAGER = '_DELM','_CLOM'
    BOOK, ARTICLE, PUBLIC, FILE, OTHER = 'BOO','ART','PU','FIL','OTH'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (DELETED_MANAGER, 'Удалённый менеджерский'),(CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    TYPE_2 = (
        (BOOK, 'Книга'),(ARTICLE, 'Статья'),(PUBLIC, 'Заметка'),(FILE, 'Файл'),(OTHER, 'Другое'),
    )

    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, validators=[validate_file_extension], verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ForeignKey(DocsList, on_delete=models.SET_NULL, related_name='docs_list', blank=True, null=True)
    type = models.CharField(choices=TYPE, max_length=5)
    type_2 = models.CharField(choices=TYPE_2, max_length=5)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")
    #community = models.ForeignKey('communities.Community', related_name='doc_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    order = models.PositiveIntegerField(default=0)
    is_doc = models.BooleanField(default=True)

    class Meta:
        ordering = ["-order"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def get_lists(self):
        return self.list.only("pk")

    def is_open(self):
        return self.type[0] != "_"
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"

    def get_mime_type(self):
        import magic

        file = self.file
        initial_pos = file.tell()
        file.seek(0)
        mime_type = magic.from_buffer(file.read(1024), mime=True)
        file.seek(initial_pos)
        return mime_type

    @classmethod
    def create_doc(cls, creator, title, file, list, community, type_2):
        from common.processing.doc import get_doc_processing

        list.count += 1
        list.save(update_fields=["count"])
        doc = cls.objects.create(creator=creator,order=list.count,title=title,list=list,file=file,community=community, type_2=type_2)
        get_doc_processing(doc, Doc.PUBLISHED)
        if community:
            from common.notify.progs import community_send_notify, community_send_wall
            from notify.models import Notify, Wall

            community.plus_docs(1)

            Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="DOC", object_id=doc.pk, verb="ITE")
            community_send_wall(doc.pk, creator.pk, community.pk, None, "create_c_doc_wall")
            for user_id in community.get_member_for_notify_ids():
                Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                community_send_notify(doc.pk, creator.pk, user_id, community.pk, None, "create_c_doc_notify")
        else:
            from common.notify.progs import user_send_notify, user_send_wall
            from notify.models import Notify, Wall

            Wall.objects.create(creator_id=creator.pk, type="DOC", object_id=doc.pk, verb="ITE")
            user_send_wall(doc.pk, None, "create_u_doc_wall")
            for user_id in creator.get_user_main_news_ids():
                Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="DOC", object_id=doc.pk, verb="ITE")
                user_send_notify(doc.pk, creator.pk, user_id, None, "create_u_doc_notify")
            creator.plus_docs(1)
        return doc

    def edit_doc(self, title, list, file):
        from common.processing.doc  import get_doc_processing

        if self.list.pk != list.pk:
            self.list.count -= 1
            self.list.save(update_fields=["count"])
            list.count += 1
            list.save(update_fields=["count"])
        self.title = title
        self.list = list
        self.file = file
        return self.save()

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = Doc.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = Doc.PUBLISHED
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def delete_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.DELETED
        elif self.type == "MAN":
            self.type = Doc.DELETED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Doc.PUBLISHED
        elif self.type == "_DELM":
            self.type = Doc.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.CLOSED
        elif self.type == "MAN":
            self.type = Doc.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if community:
            community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Doc.PUBLISHED
        elif self.type == "_CLOM":
            self.type = Doc.MANAGER
        self.save(update_fields=['type'])
        if community:
            community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")


class DocsListPerm(models.Model):
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

    list = models.ForeignKey(DocsList, related_name='+', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Список записей")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=False, verbose_name="Пользователь")

    can_see_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит список/документы")
    create_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает документы")
    can_copy = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто может добавлять список/документы себе")

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

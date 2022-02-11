import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from docs.helpers import upload_to_doc_directory, validate_file_extension
from django.db.models import Q


class DocsList(models.Model):
    MAIN, LIST, DELETED, CLOSED, CLOSED_MAIN = 'MAI','LIS','_DEL','_CLO','_CLOMA'
    ALL_CAN,FRIENDS,EACH_OTHER,FRIENDS_BUT,SOME_FRIENDS,MEMBERS,CREATOR,ADMINS,MEMBERS_BUT,SOME_MEMBERS = 1,2,3,4,5,6,7,8,9,10
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),
        (DELETED, 'Удалённый'),
        (CLOSED_MAIN, 'Закрытый основной'),
        (CLOSED, 'Закрытый'),
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
    community = models.ForeignKey('communities.Community', related_name='docs_lists_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='docs_lists_creator', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип списка")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    count = models.PositiveIntegerField(default=0)
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")

    can_see_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит документы")
    create_el = models.PositiveSmallIntegerField(choices=PERM, default=7, verbose_name="Кто создает документы и потом с этими документами работает")
    copy_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто копирует документы")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список документов"
        verbose_name_plural = "списки документов"

    def get_code(self):
        return "ldo" + str(self.pk)
    def is_doc_list(self):
        return True
    def get_description(self):
        if self.community:
            return 'список документов сообщества <a href="' + self.creator.get_link() + '" target="_blank">' + self.community.name + '</a>'
        else:
            return 'список документов <a href="' + self.creator.get_link() + '" target="_blank">' + self.creator.get_full_name_genitive() + '</a>'

    def is_user_list(self, user):
        return self in user.get_doc_lists()
    def is_user_collection_list(self, user_id):
        return user_id in self.get_users_ids()
    def is_community_list(self, community):
        return self in community.get_doc_lists()
    def is_community_collection_list(self, community_id):
        return community_id in self.get_communities_ids()

    def count_reposts(self):
        count = self.repost + self.copy
        if count == 0:
            return ''
        else:
            return count

    def change_position(query, community, user_id):
        if community:
            from communities.model.list import CommunityDocsListPosition

            for item in query:
                list = CommunityDocsListPosition.objects.get(list=item['key'], community=community.id)
                list.position = item['value']
                list.save(update_fields=["position"])
        else:
            from users.model.list import UserDocsListPosition

            for item in query:
                list = UserDocsListPosition.objects.get(list=item['key'], user=user_id)
                list.position = item['value']
                list.save(update_fields=["position"])

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

    def is_user_can_see_el(self, user_id):
        if self.creator.pk == user_id:
            return True
        elif self.community:
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

    def is_user_can_create_el(self, user_id):
        if self.creator.pk == user_id:
            return True
        elif self.community:
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

    def is_user_can_copy_el(self, user_id):
        if self.creator.pk == user_id:
            return True
        elif self.community:
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

    def is_not_empty(self):
        return self.docs_list.exclude(type__contains="_").values("pk").exists()

    def get_items(self):
        return self.docs_list.filter(type="PUB")
    def count_items(self):
        return self.docs_list.exclude(type__contains="_").values("pk").count()

    def get_users_ids(self):
        return [i['pk'] for i in self.users.exclude(type__contains="_").values("pk")]
    def get_communities_ids(self):
        return [i['pk'] for i in self.communities.exclude(type__contains="_").values("pk")]

    def add_in_community_collections(self, community):
        if (self.community and self.community.pk != community.pk) and community.pk not in [i['pk'] for i in self.communities.exclude(type__contains="_").values("pk")]:
            from communities.model.list import CommunityDocsListPosition
            self.communities.add(community)
            CommunityDocsListPosition.objects.create(community=community.pk, list=self.pk, position=DocsList.get_community_lists_count(community.pk))
    def remove_in_community_collections(self, community):
        if (self.community and self.community.pk != community.pk) and community.pk in [i['pk'] for i in self.communities.exclude(type__contains="_").values("pk")]:
            from communities.model.list import CommunityDocsListPosition
            try:
                CommunityDocsListPosition.objects.get(community=community.pk, list=self.pk).delete()
            except:
                pass
            self.communities.remove(community)
    def add_in_user_collections(self, user):
        if (self.community or self.creator.pk != user.pk) and user.pk not in [i['pk'] for i in self.users.exclude(type__contains="_").values("pk")]:
            from users.model.list import UserDocsListPosition
            self.users.add(user)
            UserDocsListPosition.objects.create(user=user.pk, list=self.pk, position=DocsList.get_user_lists_count(user.pk))
    def remove_in_user_collections(self, user):
        if (self.community or self.creator.pk != user.pk) and user.pk in [i['pk'] for i in self.users.exclude(type__contains="_").values("pk")]:
            from users.model.list import UserDocsListPosition
            try:
                UserDocsListPosition.objects.get(user=user.pk, list=self.pk).delete()
            except:
                pass
            self.users.remove(user)
    def copy_item(pk, user_or_communities):
        item = DocsList.objects.get(pk=pk)
        for object_id in user_or_communities:
            if object_id[0] == "c":
                from communities.models import Community
                community = Community.objects.get(pk=object_id[1:])
                item.add_in_community_collections(community)
            elif object_id[0] == "u":
                from users.models import User
                user = User.objects.get(pk=object_id[1:])
                item.add_in_user_collections(user)

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

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = DocsList.DELETED
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
    PUBLISHED, DELETED, CLOSED = 'PUB','_DEL','_CLO'
    BOOK, ARTICLE, PUBLIC, FILE, OTHER = 'BOO','ART','PU','FIL','OTH'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто модератором'),
    )
    TYPE_2 = (
        (BOOK, 'Книга'),(ARTICLE, 'Статья'),(PUBLIC, 'Заметка'),(FILE, 'Файл'),(OTHER, 'Другое'),
    )

    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to=upload_to_doc_directory, validators=[validate_file_extension], verbose_name="Документ")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    list = models.ForeignKey(DocsList, on_delete=models.SET_NULL, related_name='docs_list', blank=True, null=True)
    type = models.CharField(choices=TYPE, default=PUBLISHED, max_length=5)
    type_2 = models.CharField(choices=TYPE_2, default=FILE, max_length=5)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doc_creator', null=False, blank=False, verbose_name="Создатель")
    community = models.ForeignKey('communities.Community', related_name='doc_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    order = models.PositiveIntegerField(default=0)
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")

    class Meta:
        ordering = ["-order"]
        verbose_name = "Документ"
        verbose_name_plural = "Документы"
        indexes = (BrinIndex(fields=['created']),)

    def count_reposts(self):
        count = self.repost + self.copy
        if count == 0:
            return ''
        else:
            return count

    def get_code(self):
        return "doc" + str(self.pk)
    def is_doc(self):
        return True

    def is_user_can_edit_delete_item(self, user):
        if self.community and user.is_staff_of_community(self.community.pk):
            return True
        elif self.creator.pk == user.pk or self.list.creator.pk == user.pk:
            return True
        return False

    def get_description(self):
        if self.community:
            return 'документ сообщества <a href="' + self.creator.get_link() + '" target="_blank">' + self.community.name + '</a>'
        else:
            return 'документ <a href="' + self.creator.get_link() + '" target="_blank">' + self.creator.get_full_name_genitive() + '</a>'

    def copy_item(pk, lists):
        item, count = Doc.objects.get(pk=pk), 0
        for list_pk in lists:
            post_list = DocsList.objects.get(pk=list_pk)
            Doc.create_doc(
                creator=item.creator,
                list=post_list,
                title=item.title,
                file=item.file,
                type_2=item.type_2,
                community=item.community
            )
            count += 1
        item.copy += count
        item.save(update_fields=["copy"])

    def change_position(query):
        for item in query:
            doc = Doc.objects.get(pk=item['key'])
            doc.order = item['value']
            doc.save(update_fields=["order"])

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

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.DELETED
        self.save(update_fields=['type'])
        if self.community:
            self.community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Doc.PUBLISHED
        self.save(update_fields=['type'])
        if self.community:
            self.community.plus_docs(1)
        else:
            self.creator.plus_docs(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Doc.CLOSED
        self.save(update_fields=['type'])
        if self.community:
            self.community.minus_docs(1)
        else:
            self.creator.minus_docs(1)
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOC", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Doc.PUBLISHED
        self.save(update_fields=['type'])
        if self.community:
            self.community.plus_docs(1)
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

import uuid
from django.db import models
from django.conf import settings
from django.contrib.postgres.indexes import BrinIndex
from users.helpers import upload_to_user_directory
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q


class SurveyList(models.Model):
    MAIN, LIST, DELETED, CLOSED, CLOSED_MAIN = 'MAI','LIS','_DEL','_CLO','_CLOMA'
    ALL_CAN,FRIENDS,EACH_OTHER,FRIENDS_BUT,SOME_FRIENDS,MEMBERS,CREATOR,ADMINS,MEMBERS_BUT,SOME_MEMBERS = 1,2,3,4,5,6,7,8,9,10
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),
        (DELETED, 'Удалённый'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_MAIN, 'Закрытый основной'),
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
    community = models.ForeignKey('communities.Community', related_name='community_surveylist', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator_surveylist', on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип списка")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')
    count = models.PositiveIntegerField(default=0)
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")

    can_see_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто видит записи")
    create_el = models.PositiveSmallIntegerField(choices=PERM, default=7, verbose_name="Кто создает записи и потом с этими документами работает")
    copy_el = models.PositiveSmallIntegerField(choices=PERM, default=1, verbose_name="Кто может копировать")

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "список опросов"
        verbose_name_plural = "списки опросов"

    def get_code(self):
        return "lsu" + str(self.pk)
    def is_survey_list(self):
        return True

    def get_description(self):
        if self.community:
            return 'список опросов сообщества <a href="' + self.community.get_link() + '" target="_blank">' + self.community.name + '</a>'
        else:
            return 'список опросов <a href="' + self.creator.get_link() + '" target="_blank">' + self.creator.get_full_name_genitive() + '</a>'

    def is_user_list(self, user):
        return self in user.get_survey_lists()
    def is_user_collection_list(self, user_id):
        return user_id in self.get_users_ids()
    def is_community_list(self, community):
        return self in community.get_survey_lists()
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
            from communities.model.list import CommunitySurveyListPosition

            for item in query:
                list = CommunitySurveyListPosition.objects.get(list=item['key'], community=community.id)
                list.position = item['value']
                list.save(update_fields=["position"])
        else:
            from users.model.list import UserSurveyListPosition

            for item in query:
                list = UserSurveyListPosition.objects.get(list=item['key'], user=user_id)
                list.position = item['value']
                list.save(update_fields=["position"])

    def get_can_see_el_exclude_users_ids(self):
        list = SurveyListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_include_users_ids(self):
        list = SurveyListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_exclude_users_ids())
    def get_can_see_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_include_users_ids())

    def get_create_el_exclude_users_ids(self):
        list = SurveyListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_include_users_ids(self):
        list = SurveyListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_exclude_users_ids())
    def get_create_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_include_users_ids())

    def get_copy_el_exclude_users_ids(self):
        list = SurveyListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_include_users_ids(self):
        list = SurveyListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
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

    def count_items_ru(self):
        count = self.count_items()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " опрос"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " опроса"
        else:
            return str(count) + " опросов"

    def add_in_community_collections(self, community):
        if (self.community and self.community.pk != community.pk) and community.pk not in [i['pk'] for i in self.communities.exclude(type__contains="_").values("pk")]:
            from communities.model.list import CommunitySurveyListPosition
            self.communities.add(community)
            CommunitySurveyListPosition.objects.create(community=community.pk, list=self.pk, position=SurveyList.get_community_lists_count(community.pk))
    def remove_in_community_collections(self, community):
        if (self.community and self.community.pk != community.pk) and community.pk in [i['pk'] for i in self.communities.exclude(type__contains="_").values("pk")]:
            from communities.model.list import CommunitySurveyListPosition
            try:
                CommunitySurveyListPosition.objects.get(community=community.pk, list=self.pk).delete()
            except:
                pass
            self.communities.remove(community)
    def add_in_user_collections(self, user):
        if (self.community or self.creator.pk != user.pk) and user.pk not in [i['pk'] for i in self.users.exclude(type__contains="_").values("pk")]:
            from users.model.list import UserSurveyListPosition
            self.users.add(user)
            UserSurveyListPosition.objects.create(user=user.pk, list=self.pk, position=SurveyList.get_user_lists_count(user.pk))
    def remove_in_user_collections(self, user):
        if (self.community or self.creator.pk != user.pk) and user.pk in [i['pk'] for i in self.users.exclude(type__contains="_").values("pk")]:
            from users.model.list import UserSurveyListPosition
            try:
                UserSurveyListPosition.objects.get(user=user.pk, list=self.pk).delete()
            except:
                pass
            self.users.remove(user)
    def copy_item(pk, user_or_communities):
        item = SurveyList.objects.get(pk=pk)
        for object_id in user_or_communities:
            if object_id[0] == "c":
                from communities.models import Community
                community = Community.objects.get(pk=object_id[1:])
                item.add_in_community_collections(community)
            elif object_id[0] == "u":
                from users.models import User
                user = User.objects.get(pk=object_id[1:])
                item.add_in_user_collections(user)

    def is_not_empty(self):
        return self.survey_list.exclude(type__contains="_").values("pk").exists()

    def get_items(self):
        return self.survey_list.filter(type="PUB")
    def count_items(self):
        return self.survey_list.exclude(type__contains="_").values("pk").count()

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
    def is_private(self):
        return False
    def is_open(self):
        return self.type[0] != "_"
    def is_have_edit(self):
        return self.is_list() or self.is_private()
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        try:
            from users.model.list import UserSurveyListPosition
            query = []
            lists = UserSurveyListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from users.model.list import UserSurveyListPosition
            query = []
            lists = UserSurveyListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from communities.model.list import CommunitySurveyListPosition
            query = []
            lists = CommunitySurveyListPosition.objects.filter(community=community_pk, type=1).values("list")
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
            from communities.model.list import CommunitySurveyListPosition
            query = []
            lists = CommunitySurveyListPosition.objects.filter(community=community_pk, type=1).values("list")
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
    def create_list(cls, creator, name, description, community):
        from notify.models import Notify, Wall
        from common.processing.survey import get_survey_list_processing

        list = cls.objects.create(creator=creator,name=name,description=description, community=community)
        is_public = True
        if community:
            from communities.model.list import CommunitySurveyListPosition
            CommunitySurveyListPosition.objects.create(community=community.pk, list=list.pk, position=SurveyList.get_community_lists_count(community.pk))
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="SUL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_survey_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="SUL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_survey_list_notify")
        else:
            from users.model.list import UserSurveyListPosition
            UserSurveyListPosition.objects.create(user=creator.pk, list=list.pk, position=SurveyList.get_user_lists_count(creator.pk))
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="SUL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_survey_list_wall")
                for user_id in creator.get_user_main_news_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="SUL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_survey_list_notify")
        get_survey_list_processing(list, SurveyList.LIST)
        return list

    def edit_list(self, name, description):
        self.name = name
        self.description = description
        self.save()
        return self

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SurveyList.DELETED
        elif self.type == "MAN":
            self.type = SurveyList.DELETED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunitySurveyListPosition
            CommunitySurveyListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserSurveyListPosition
            UserSurveyListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "TDEL":
            self.type = SurveyList.LIST
        elif self.type == "TDELM":
            self.type = SurveyList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunitySurveyListPosition
            CommunitySurveyListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserSurveyListPosition
            UserSurveyListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SurveyList.CLOSED
        elif self.type == "MAI":
            self.type = SurveyList.CLOSED_MAIN
        elif self.type == "MAN":
            self.type = SurveyList.CLOSED_MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunitySurveyListPosition
            CommunitySurveyListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserSurveyListPosition
            UserSurveyListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "TCLO":
            self.type = SurveyList.LIST
        elif self.type == "TCLOM":
            self.type = SurveyList.MAIN
        elif self.type == "TCLOM":
            self.type = SurveyList.MANAGER
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunitySurveyListPosition
            CommunitySurveyListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserSurveyListPosition
            UserSurveyListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUL", object_id=self.pk, verb="ITE").update(status="R")


class Survey(models.Model):
    PUBLISHED = 'PUB'
    DELETED = '_DEL'
    CLOSED = '_CLO'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),
        (DELETED, 'Удалено'),
        (CLOSED, 'Закрыто модератором'),
    )
    title = models.CharField(max_length=250, verbose_name="Название")
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='survey_creator', verbose_name="Создатель")
    is_anonymous = models.BooleanField(verbose_name="Анонимный", default=False)
    is_multiple = models.BooleanField(verbose_name="Несколько вариантов", default=False)
    is_no_edited = models.BooleanField(verbose_name="Запрет отмены голоса", default=False)
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядковый номер")
    image = ProcessedImageField(verbose_name='Главное изображение', blank=True, format='JPEG',options={'quality': 90}, processors=[Transpose(), ResizeToFit(512,512)],upload_to=upload_to_user_directory)
    type = models.CharField(choices=TYPE, default=PUBLISHED, max_length=5)
    time_end = models.DateTimeField(null=True, blank=True, verbose_name="Дата окончания")
    list = models.ForeignKey(SurveyList, on_delete=models.CASCADE, related_name='survey_list', verbose_name="Список")
    community = models.ForeignKey('communities.Community', related_name='survey_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    vote = models.PositiveIntegerField(default=0, verbose_name="Кол-во голосов")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")

    class Meta:
        indexes = (BrinIndex(fields=['created']),)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ["-order"]

    def __str__(self):
        return self.title

    def is_can_edit(self):
        from datetime import datetime, timedelta
        return datetime.now() < self.created + timedelta(minutes=60)

    def get_code(self):
        return "sur" + str(self.pk)
    def is_survey(self):
        return True

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/static/images/no_img/list.jpg'

    def is_user_can_edit_delete_item(self, user):
        if self.community and user.is_staff_of_community(self.community.pk):
            return True
        elif self.creator.pk == user.pk or self.list.creator.pk == user.pk:
            return True
        return False

    def get_description(self):
        if self.community:
            return 'опрос сообщества <a href="' + self.community.get_link() + '" target="_blank">' + self.community.name + '</a>'
        else:
            return 'опрос <a href="' + self.creator.get_link() + '" target="_blank">' + self.creator.get_full_name_genitive() + '</a>'

    def change_position(query):
        for item in query:
            i = Survey.objects.get(pk=item['key'])
            i.order = item['value']
            i.save(update_fields=["order"])

    def count_reposts(self):
        count = self.repost + self.copy
        if count == 0:
            return ''
        else:
            return count

    def plus_reposts(self, count):
        self.repost += count
        return self.save(update_fields=['repost'])
    def minus_reposts(self, count):
        self.repost -= count
        return self.save(update_fields=['repost'])
    def plus_votes(self, count):
        self.vote += count
        return self.save(update_fields=['vote'])
    def minus_votes(self, count):
        self.vote -= count
        return self.save(update_fields=['vote'])

    @classmethod
    def create_survey(cls, title, list, image, creator, is_anonymous, is_multiple, is_no_edited, time_end, answers, community):
        list.count += 1
        list.save(update_fields=["count"])
        survey = cls.objects.create(title=title,order=list.count,list=list,image=image,creator=creator,is_anonymous=is_anonymous,is_multiple=is_multiple,is_no_edited=is_no_edited,time_end=time_end)
        answer_order = 0
        for answer in answers:
            answer_order += 1
            Answer.objects.create(survey=survey, text=answer, order=answer_order)
        if community:
            from common.notify.progs import community_send_notify, community_send_wall
            from notify.models import Notify, Wall

            Wall.objects.create(creator_id=creator.pk, community_id=community.pk, type="SUR", object_id=survey.pk, verb="ITE")
            community_send_wall(doc.pk, creator.pk, community.pk, None, "create_c_survey_wall")
            for user_id in community.get_member_for_notify_ids():
                Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="SUR", object_id=survey.pk, verb="ITE")
                community_send_notify(doc.pk, creator.pk, user_id, community.pk, None, "create_c_survey_notify")
        else:
            from common.notify.progs import user_send_notify, user_send_wall
            from notify.models import Notify, Wall

            Wall.objects.create(creator_id=creator.pk, type="SUR", object_id=survey.pk, verb="ITE")
            user_send_wall(survey.pk, None, "create_u_survey_wall")
            for user_id in creator.get_user_main_news_ids():
                Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="SUR", object_id=survey.pk, verb="ITE")
                user_send_notify(survey.pk, creator.pk, user_id, None, "create_u_survey_notify")
        return survey

    def edit_survey(self, title, image, is_anonymous, is_multiple, is_no_edited, time_end, answers):
        self.title = title
        self.image = image
        self.is_anonymous = is_anonymous
        self.is_multiple = is_multiple
        self.is_no_edited = is_no_edited
        self.time_end = time_end
        self.save()

        answer_order = 0
        Answer.objects.filter(survey=self).delete()
        for answer in answers:
            answer_order += 1
            Answer.objects.create(survey=self, text=answer, order=answer_order)
        return self

    def is_user_voted(self, user_id):
        return not self.is_time_end() and SurveyVote.objects.filter(answer__survey_id=self.pk, user_id=user_id).exists()

    def is_time_end(self):
        if self.time_end:
            from datetime import datetime
            now = datetime.now()
            return self.time_end < now
        else:
            return False

    def get_answers(self):
        return Answer.objects.filter(survey_id=self.pk)
    def get_answers_count(self):
        return self.get_answers().values("pk").count()
    def is_full_answers(self):
        return self.get_answers_count() > 9

    def get_all_count(self):
        if self.vote > 0:
            return self.vote

    def get_users(self):
        from users.models import User
        voter_ids = SurveyVote.objects.filter(answer__survey_id=self.pk).values("user_id")
        return User.objects.filter(id__in=[i['user_id'] for i in voter_ids])

    def get_6_users(self):
        from users.models import User
        voter_ids = SurveyVote.objects.filter(answer__survey_id=self.pk).values("user_id")[:6]
        list = ''
        for voter in User.objects.filter(id__in=[i['user_id'] for i in voter_ids]):
            list += '<a class="pr-1" href="' + voter.get_link() + '" target="_blank" tooltip="' + voter.get_full_name() + '" flow="up"><figure style="margin: 0;">' + voter.get_s_avatar() + '</figure></a>'
        return list

    def is_have_votes(self):
        return SurveyVote.objects.filter(answer__survey_id=self.pk).values("id").exists()

    def delete_item(self):
        from notify.models import Notify, Wall
        self.type = Survey.DELETED
        self.save(update_fields=['type'])
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        self.type = Survey.PUBLISHED
        self.save(update_fields=['type'])
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Survey.CLOSED
        self.save(update_fields=['type'])
        self.list.count -= 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "TCLO":
            self.type = Survey.PUBLISHED
        self.save(update_fields=['type'])
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="SUR", object_id=self.pk, verb="ITE").update(status="R")

    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"

    def votes_create(self, user, votes):
        import json
        from datetime import datetime
        from django.http import HttpResponse

        if (self.time_end and self.time_end < datetime.now()) or user.is_voted_of_survey(self.pk):
            return HttpResponse()
        data = []

        self.vote += 1
        self.save(update_fields=["vote"])

        for answer_id in votes:
            answer = Answer.objects.get(pk=answer_id)
            SurveyVote.objects.create(answer_id=answer_id, user=user)
            answer.vote += 1
            answer.save(update_fields=["vote"])
            data.append(str(answer_id) + "," + str(answer.get_count()) + "," + str(answer.get_procent()) + ";")
        if self.community:
            from common.notify.notify import community_notify, community_wall

            community = self.community
            community_notify(user, community, None, self.pk, "SUR", "c_survey_vote_notify", "SVO")
            community_wall(user, community, None, self.pk, "SUR", "c_survey_vote_wall", "SVO")
        else:
            from common.notify.notify import user_notify, user_wall

            user_notify(user, None, self.pk, "SUR", "u_survey_vote_notify", "SVO")
            user_wall(user, None, self.pk, "SUR", "u_survey_vote_wall", "SVO")

        return HttpResponse(data)
    def votes_delete(self, user):
        from django.http import HttpResponse

        if not user.is_voted_of_survey(self.pk) or self.is_no_edited:
            return HttpResponse()
        self.vote -= 1
        self.save(update_fields=["vote"])

        data = []
        for answer in self.get_answers():
            if SurveyVote.objects.filter(answer_id=answer.pk, user=user).exists():
                SurveyVote.objects.filter(answer_id=answer.pk, user=user).delete()
                try:
                    answer.vote -= 1
                    answer.save(update_fields=["vote"])
                except:
                    pass
            data.append(str(answer.pk) + "," + str(answer.get_count()) + "," + str(answer.get_procent()) + ";")
        return HttpResponse(data)


class Answer(models.Model):
    text = models.CharField(max_length=250, verbose_name="Вариант ответа")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='+', verbose_name="Опрос")
    vote = models.PositiveIntegerField(default=0, verbose_name="Кол-во голосов")
    order = models.PositiveIntegerField(default=0, verbose_name="Градация по порядку")

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ["order"]

    def __str__(self):
        return self.text

    def get_count(self):
        return self.vote

    def is_user_voted(self, user_id):
        return SurveyVote.objects.filter(answer_id=self.pk, user_id=user_id).exists()

    def get_answers(self):
        return SurveyVote.objects.filter(answer_id=self.pk)

    def get_procent(self):
        if self.vote:
            count = self.vote / self.survey.vote * 100
            return int(count)
        else:
            return 0

    def plus_votes(self, count):
        self.vote += count
        return self.save(update_fields=['vote'])
    def minus_votes(self, count):
        self.vote -= count
        return self.save(update_fields=['vote'])


class SurveyVote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, related_name='user_voter', verbose_name="Участник опроса")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, db_index=False, related_name='user_answer', verbose_name="Опрос")

    def __str__(self):
        return self.user.get_full_name()

    @classmethod
    def create_answer(cls, user, answer):
        return cls.objects.create(user=user, answer=answer)

    class Meta:
        unique_together = (('user', 'answer'),)
        indexes = [
            models.Index(fields=['answer', 'user']),
            ]
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'

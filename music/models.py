import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from music.helpers import upload_to_music_directory, validate_file_extension
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models import Q


class SoundGenres(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_tracks_count(self):
        return self.track_genre.count()

    def is_track_in_genre(self, track_id):
        self.track_genre.filter(id=track_id).exists()

    def get_items(self):
        queryset = self.track_genre.all()
        return queryset[:300]

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"


class Artist(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 96}, upload_to="music/artist/", processors=[Transpose(), ResizeToFit(width=500, height=500)])
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Исполнитель"
        verbose_name_plural = "Исполнители"

class MusicAlbum(models.Model):
    name = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, related_name='artist_playlist', blank=True, null=True, db_index=False, on_delete=models.CASCADE, verbose_name="Исполнитель")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_playlist_album', db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to="music/artist/", processors=[Transpose(), ResizeToFit(width=400, height=400)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "плейлист"
        verbose_name_plural = "плейлисты"
        indexes = (BrinIndex(fields=['created']),)


class MusicList(models.Model):
    MAIN, LIST, DELETED, CLOSED, CLOSED_MAIN, SUSPENDED, SUSPENDED_MAIN = 'MAI','LIS','_DEL','_CLO','_CLOMA','_SUS','_SUSMA'
    ALL_CAN,FRIENDS,EACH_OTHER,FRIENDS_BUT,SOME_FRIENDS,MEMBERS,CREATOR,ADMINS,MEMBERS_BUT,SOME_MEMBERS = 1,2,3,4,5,6,7,8,9,10
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),
        (DELETED, 'Удалённый'),
        (CLOSED, 'Закрытый менеджером'),(CLOSED_MAIN, 'Закрытый основной'),
        (SUSPENDED_MAIN, 'Замороженный основной'),(SUSPENDED, 'Замороженный'),
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
    community = models.ForeignKey('communities.Community', related_name='community_playlist', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_playlist', db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, verbose_name="Тип списка")
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=400, height=400)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
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
        verbose_name = "плейлист"
        verbose_name_plural = "плейлисты"

    def get_code(self):
        return "lmu" + str(self.pk)
    def is_music_list(self):
        return True

    def get_longest_penalties(self):
        from managers.models import ModerationPenalty
        return ModerationPenalty.objects.filter(type="MUL", object_id=self.pk)[0].get_expiration()
    def get_moderated_description(self):
        from managers.models import Moderated
        obj = Moderated.objects.filter(type="MUL", object_id=self.pk)[0]
        if obj.description:
            return obj.description
        else:
            return "Предупреждение за нарушение правил соцсети трезвый.рус"

    def get_description(self):
        if self.community:
            return 'плейлист сообщества <a href="' + self.community.get_link() + '" target="_blank">' + self.community.name + '</a>'
        else:
            return 'плейлист <a href="' + self.creator.get_link() + '" target="_blank">' + self.creator.get_full_name_genitive() + '</a>'

    def is_user_list(self, user):
        return self in user.get_playlists()
    def is_user_collection_list(self, user_id):
        return user_id in self.get_users_ids()
    def is_community_list(self, community):
        return self in community.get_playlists()
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
            from communities.model.list import CommunityPlayListPosition

            for item in query:
                list = CommunityPlayListPosition.objects.get(list=item['key'], community=community.id)
                list.position = item['value']
                list.save(update_fields=["position"])
        else:
            from users.model.list import UserPlayListPosition

            for item in query:
                list = UserPlayListPosition.objects.get(list=item['key'], user=user_id)
                list.position = item['value']
                list.save(update_fields=["position"])

    def count_items_ru(self):
        count = self.count_items()
        a, b = count % 10, count % 100
        if (a == 1) and (b != 11):
            return str(count) + " аудиозапись"
        elif (a >= 2) and (a <= 4) and ((b < 10) or (b >= 20)):
            return str(count) + " аудиозаписи"
        else:
            return str(count) + " аудиозаписей"

    def get_can_see_el_exclude_users_ids(self):
        list = MusicListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_include_users_ids(self):
        list = MusicListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_can_see_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_exclude_users_ids())
    def get_can_see_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_can_see_el_include_users_ids())

    def get_create_el_exclude_users_ids(self):
        list = MusicListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_include_users_ids(self):
        list = MusicListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
        return [i['user_id'] for i in list]
    def get_create_el_exclude_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_exclude_users_ids())
    def get_create_el_include_users(self):
        from users.models import User
        return User.objects.filter(id__in=self.get_create_el_include_users_ids())

    def get_copy_el_exclude_users_ids(self):
        list = MusicListPerm.objects.filter(list_id=self.pk, can_see_item=2).values("user_id")
        return [i['user_id'] for i in list]
    def get_copy_el_include_users_ids(self):
        list = MusicListPerm.objects.filter(list_id=self.pk, can_see_item=1).values("user_id")
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

    def add_in_community_collections(self, community):
        if (self.community and self.community.pk != community.pk) and community.pk not in [i['pk'] for i in self.communities.exclude(type__contains="_").values("pk")]:
            from communities.model.list import CommunityPlayListPosition
            self.communities.add(community)
            CommunityPlayListPosition.objects.create(community=community.pk, list=self.pk, position=MusicList.get_community_lists_count(community.pk))
    def remove_in_community_collections(self, community):
        if (self.community and self.community.pk != community.pk) and community.pk in [i['pk'] for i in self.communities.exclude(type__contains="_").values("pk")]:
            from communities.model.list import CommunityPlayListPosition
            try:
                CommunityPlayListPosition.objects.get(community=community.pk, list=self.pk).delete()
            except:
                pass
            self.communities.remove(community)
    def add_in_user_collections(self, user):
        if (self.community or self.creator.pk != user.pk) and user.pk not in [i['pk'] for i in self.users.exclude(type__contains="_").values("pk")]:
            from users.model.list import UserPlayListPosition
            self.users.add(user)
            UserPlayListPosition.objects.create(user=user.pk, list=self.pk, position=MusicList.get_user_lists_count(user.pk))
    def remove_in_user_collections(self, user):
        if (self.community or self.creator.pk != user.pk) and user.pk in [i['pk'] for i in self.users.exclude(type__contains="_").values("pk")]:
            from users.model.list import UserPlayListPosition
            try:
                UserPlayListPosition.objects.get(user=user.pk, list=self.pk).delete()
            except:
                pass
            self.users.remove(user)
    def copy_item(pk, user_or_communities):
        item = MusicList.objects.get(pk=pk)
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
        return self.playlist.filter(Q(type="PUB")|Q(type="PRI")).values("pk").exists()
    def get_items(self):
        return self.playlist.filter(type="PUB")
    def get_6_items(self):
        return self.playlist.filter(type="PUB")[:6]
    def count_items(self):
        return self.playlist.filter(Q(type="PUB")|Q(type="PRI")).values("pk").count()

    def get_users_ids(self):
        users = self.users.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in users]
    def get_communities_ids(self):
        communities = self.communities.exclude(type__contains="_").values("pk")
        return [i['pk'] for i in communities]

    def get_remote_image(self, image_url):
        import os
        from django.core.files import File
        from urllib import request

        result = request.urlretrieve(image_url)
        self.image.save(
            os.path.basename(image_url),
            File(open(result[0], 'rb'))
        )
        self.save()

    def is_main(self):
        return self.type == self.MAIN
    def is_list(self):
        return self.type == self.LIST
    def is_open(self):
        return self.type[0] != "_"
    def is_have_edit(self):
        return self.is_list()
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"
    def is_suspended(self):
        return self.type[:4] == "_SUS"

    @classmethod
    def create_list(cls,creator,name,description,community,can_see_el,create_el,copy_el,can_see_el_users,create_el_users,copy_el_users):
        from common.processing.music import get_playlist_processing

        list = cls.objects.create(creator=creator,name=name,description=description, community=community,can_see_el=can_see_el,create_el=create_el,copy_el=copy_el)
        get_playlist_processing(list, MusicList.LIST)
        if community:
            from communities.model.list import CommunityPlayListPosition
            CommunityPlayListPosition.objects.create(community=community.pk, list=list.pk, position=MusicList.get_community_lists_count(community.pk))
        else:
            from users.model.list import UserPlayListPosition
            UserPlayListPosition.objects.create(user=creator.pk, list=list.pk, position=MusicList.get_user_lists_count(creator.pk))

        if can_see_el == 4 or can_see_el == 9:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = MusicListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                for user_id in can_see_el_users:
                    perm = MusicListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                list.can_see_el = 7
                list.save(update_fields=["can_see_el"])

        if create_el == 4 or create_el == 9:
            if create_el_users:
                for user_id in create_el_users:
                    perm = MusicListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                for user_id in create_el_users:
                    perm = MusicListPerm.get_or_create_perm(list.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                list.create_el = 7
                list.save(update_fields=["create_el"])

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = MusicListPerm.get_or_create_perm(list.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                list.copy_el = 7
                list.save(update_fields=["copy_el"])
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                for user_id in copy_el_users:
                    perm = MusicListPerm.get_or_create_perm(list.pk, user_id)
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
                MusicListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = MusicListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 2
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7
        elif can_see_el == 5 or can_see_el == 10:
            if can_see_el_users:
                MusicListPerm.objects.filter(list_id=self.pk).update(can_see_item=0)
                for user_id in can_see_el_users:
                    perm = MusicListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_see_item = 1
                    perm.save(update_fields=["can_see_item"])
            else:
                self.can_see_el = 7

        if create_el == 4 or create_el == 9:
            if create_el_users:
                MusicListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = MusicListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 2
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7
        elif create_el == 5 or create_el == 10:
            if create_el_users:
                MusicListPerm.objects.filter(list_id=self.pk).update(create_item=0)
                for user_id in create_el_users:
                    perm = MusicListPerm.get_or_create_perm(self.pk, user_id)
                    perm.create_item = 1
                    perm.save(update_fields=["create_item"])
            else:
                self.create_el = 7

        if copy_el == 4 or copy_el == 9:
            if copy_el_users:
                MusicListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = MusicListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 2
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7
        elif copy_el == 5 or copy_el == 10:
            if copy_el_users:
                MusicListPerm.objects.filter(list_id=self.pk).update(can_copy=0)
                for user_id in copy_el_users:
                    perm = MusicListPerm.get_or_create_perm(self.pk, user_id)
                    perm.can_copy = 1
                    perm.save(update_fields=["can_copy"])
            else:
                self.copy_el = 7

        self.save()
        return self

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS" or self.type == "_CLO" or self.type == "_SUS":
            self.type = MusicList.DELETED
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPlayListPosition
            CommunityPlayListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserPlayListPosition
            UserPlayListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = MusicList.LIST
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPlayListPosition
            CommunityPlayListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserPlayListPosition
            UserPlayListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS" or self.type == "_SUS":
            self.type = MusicList.CLOSED
        elif self.type == "MAI" or self.type == "_SUSMA":
            self.type = MusicList.CLOSED_MAIN
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPlayListPosition
            CommunityPlayListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserPlayListPosition
            UserPlayListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO" or self.type == "_SUS":
            self.type = MusicList.LIST
        elif self.type == "_CLOMA" or self.type == "_SUSMA":
            self.type = MusicList.MAIN
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPlayListPosition
            CommunityPlayListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserPlayListPosition
            UserPlayListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    def suspend_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS" or self.type == "_CLO":
            self.type = MusicList.SUSPENDED
        elif self.type == "MAI" or self.type == "_CLOMA":
            self.type = MusicList.SUSPENDED_MAIN
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPlayListPosition
            CommunityPlayListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=0)
        else:
            from users.model.list import UserPlayListPosition
            UserPlayListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=0)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def unsuspend_item(self):
        from notify.models import Notify, Wall
        if self.type == "_SUS" or self.type == "_CLO":
            self.type = MusicList.LIST
        elif self.type == "_SUSMA" or self.type == "_CLOMA":
            self.type = MusicList.MAIN
        self.save(update_fields=['type'])
        if self.community:
            from communities.model.list import CommunityPlayListPosition
            CommunityPlayListPosition.objects.filter(community=self.community.pk, list=self.pk).update(type=1)
        else:
            from users.model.list import UserPlayListPosition
            UserPlayListPosition.objects.filter(user=self.creator.pk, list=self.pk).update(type=1)
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        try:
            from users.model.list import UserPlayListPosition
            query = []
            lists = UserPlayListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from users.model.list import UserPlayListPosition
            query = []
            lists = UserPlayListPosition.objects.filter(user=user_pk, type=1).values("list")
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
            from communities.model.list import CommunityPlayListPosition
            query = []
            lists = CommunityPlayListPosition.objects.filter(community=community_pk, type=1).values("list")
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
            from communities.model.list import CommunityPlayListPosition
            query = []
            lists = CommunityPlayListPosition.objects.filter(community=community_pk, type=1).values("list")
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


class UserTempMusicList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_of_field', db_index=False, on_delete=models.CASCADE, verbose_name="Слушатель")
    list = models.ForeignKey(MusicList, related_name='list_field', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Связь на плейлист человека или сообщества")
    genre = models.ForeignKey(SoundGenres, related_name='genre_field', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Связь на жанр")


class Music(models.Model):
    PUBLISHED, DELETED, CLOSED = 'PUB','_DEL','_CLO'
    TYPE = (
        (PUBLISHED, 'Опубликовано'),(DELETED, 'Удалено'),(CLOSED, 'Закрыто модератором'),
    )
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=100, height=100)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    duration = models.CharField(max_length=255, blank=True, null=True)
    genre = models.ForeignKey(SoundGenres, blank=True, null=True, related_name='track_genre', on_delete=models.CASCADE, verbose_name="Жанр трека")
    title = models.CharField(max_length=255)
    list = models.ForeignKey(MusicList, on_delete=models.SET_NULL, related_name='playlist', blank=True, null=True)
    album = models.ForeignKey(MusicAlbum, on_delete=models.SET_NULL, related_name='album_playlist', blank=True, null=True)
    type = models.CharField(choices=TYPE, default=PUBLISHED, max_length=5)
    file = models.FileField(upload_to=upload_to_music_directory, blank=True, validators=[validate_file_extension], verbose_name="Аудиозапись")
    community = models.ForeignKey('communities.Community', related_name='music_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_track', blank=True, null=True, on_delete=models.CASCADE, verbose_name="Создатель")

    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")
    copy = models.PositiveIntegerField(default=0, verbose_name="Кол-во копий")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "спарсенные треки"
        verbose_name_plural = "спарсенные треки"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ["-order"]

    def __str__(self):
        return self.title

    def copy_item(pk, lists):
        item, count = Music.objects.get(pk=pk), 0
        for list_pk in lists:
            post_list = MusicList.objects.get(pk=list_pk)
            Music.create_track(
                creator=item.creator,
                list=post_list,
                genre=item.genre,
                title=item.title,
                album=item.album,
                file=item.file,
                community=item.community
            )
            count += 1
        item.copy += count
        item.save(update_fields=["copy"])

    def get_code(self):
        return "mus" + str(self.pk)
    def is_track(self):
        return True

    def is_user_can_edit_delete_item(self, user):
        if self.community and user.is_staff_of_community(self.community.pk):
            return True
        elif self.creator.pk == user.pk or self.list.creator.pk == user.pk:
            return True
        return False

    def get_description(self):
        if self.community:
            return 'аудиозапись сообщества <a href="' + self.community.get_link() + '" target="_blank">' + self.community.name + '</a>'
        else:
            return 'аудиозапись <a href="' + self.creator.get_link() + '" target="_blank">' + self.creator.get_full_name_genitive() + '</a>'

    def change_position(query):
        for item in query:
            i = Music.objects.get(pk=item['key'])
            i.order = item['value']
            i.save(update_fields=["order"])

    def count_reposts(self):
        count = self.repost + self.copy
        if count == 0:
            return ''
        else:
            return count

    def get_s_image(self):
        if self.image:
            return '<img style="width:30px;" alt="image" src="' + self.image.url + '" />'
        elif self.album:
            if self.album.image:
                return '<img style="width:30px;" alt="image" src="' + self.album.image.url + '" />'
            elif self.album.artist and self.album.artist.image:
                return '<img style="width:30px;" alt="image" src="' + self.album.artist.image.url + '" />'
            else:
                return '<svg fill="currentColor" class="svg_default" width="30" height="30" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"></path></svg>'
        else:
            return '<svg fill="currentColor" class="svg_default" width="30" height="30" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"></path></svg>'

    def get_image(self):
        if self.image:
            return '<img style="width:40px;" alt="image" src="' + self.image.url + '" />'
        elif self.album:
            if self.album.image:
                return '<img style="width:40px;" alt="image" src="' + self.album.image.url + '" />'
            elif self.album.artist and self.album.artist.image:
                return '<img style="width:40px;" alt="image" src="' + self.album.artist.image.url + '" />'
            else:
                return '<svg fill="currentColor" class="svg_default" width="40" height="40" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"></path></svg>'
        else:
            return '<svg fill="currentColor" class="svg_default" width="40" height="40" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"></path><path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"></path></svg>'

    def get_duration(self):
        return "0"

    def get_remote_image(self, image_url):
        import os
        from django.core.files import File
        from urllib import request

        result = request.urlretrieve(image_url)
        self.image.save(
            os.path.basename(image_url),
            File(open(result[0], 'rb'))
        )
        self.save()

    def delete_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB" or self.type == "_CLO":
            self.type = Music.DELETED
        self.save(update_fields=['type'])
        if self.community:
            self.community.minus_tracks(1)
        else:
            self.creator.minus_tracks(1)
        if self.list.count > 0:
            self.list.count -= 1
            self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def restore_item(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = Music.PUBLISHED
        self.save(update_fields=['type'])
        if self.community:
            self.community.plus_tracks(1)
        else:
            self.creator.plus_tracks(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "PUB":
            self.type = Music.CLOSED
        self.save(update_fields=['type'])
        if self.community:
            self.community.minus_tracks(1)
        else:
            self.creator.minus_tracks(1)
        if self.list.count > 0:
            self.list.count -= 1
            self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = Music.PUBLISHED
        self.save(update_fields=['type'])
        if self.community:
            self.community.plus_tracks(1)
        else:
            self.creator.plus_tracks(1)
        self.list.count += 1
        self.list.save(update_fields=["count"])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def is_open(self):
        return self.type[0] != "_"
    def is_deleted(self):
        return self.type[:4] == "_DEL"
    def is_closed(self):
        return self.type[:4] == "_CLO"


class MusicListPerm(models.Model):
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

    list = models.ForeignKey(MusicList, related_name='+', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Список записей")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='+', null=True, blank=False, verbose_name="Пользователь")

    can_see_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит список/аудиозаписи")
    can_see_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто видит комментарии")
    create_item = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает аудиозаписи")
    create_comment = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто создает комментарии")
    can_copy = models.PositiveSmallIntegerField(choices=ITEM, default=0, verbose_name="Кто может добавлять список/аудиозаписи себе")

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

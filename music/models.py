import uuid
from django.conf import settings
from django.db import models
from django.contrib.postgres.indexes import BrinIndex
from music.helpers import upload_to_music_directory, validate_file_extension
from pilkit.processors import ResizeToFill, ResizeToFit, Transpose
from imagekit.models import ProcessedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from communities.models import Community


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


class SoundSymbol(models.Model):
    RUS_SYMBOL = 'RS'
    ANGL_SYMBOL = 'AS'
    NUMBER_SYMBOL = 'NS'
    SYMBOL_TYPES = (
        (RUS_SYMBOL, 'русские исполнители'),
        (ANGL_SYMBOL, 'английские исполнители'),
        (NUMBER_SYMBOL, 'исполнители по цифрам'),
        )

    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=5, choices=SYMBOL_TYPES, default=ANGL_SYMBOL, verbose_name="Язык исполнителя")

    def __str__(self):
        return self.name

    def get_tags_count(self):
        return self.symbol_papa.count()

    class Meta:
        verbose_name = "буква поиска музыки"
        verbose_name_plural = "буквы поиска музыки"


class SoundList(models.Model):
    MAIN, LIST, MANAGER, THIS_PROCESSING, PRIVATE = 'MAI', 'LIS', 'MAN', '_PRO', 'PRI'
    THIS_DELETED, THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER = '_DEL', '_DELP', '_DELM'
    THIS_CLOSED, THIS_CLOSED_PRIVATE, THIS_CLOSED_MAIN, THIS_CLOSED_MANAGER = '_CLO', '_CLOP', '_CLOM', '_CLOMA'
    TYPE = (
        (MAIN, 'Основной'),(LIST, 'Пользовательский'),(PRIVATE, 'Приватный'),(MANAGER, 'Созданный персоналом'),(THIS_PROCESSING, 'Обработка'),
        (THIS_DELETED, 'Удалённый'),(THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),
        (THIS_CLOSED, 'Закрытый менеджером'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MAIN, 'Закрытый основной'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', related_name='community_playlist', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_playlist', db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")
    type = models.CharField(max_length=6, choices=TYPE, default=THIS_PROCESSING, verbose_name="Тип списка")
    order = models.PositiveIntegerField(default=0)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name="uuid")
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=400, height=400)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Создан")
    description = models.CharField(max_length=200, blank=True, verbose_name="Описание")

    users = models.ManyToManyField("users.User", blank=True, related_name='+')
    communities = models.ManyToManyField('communities.Community', blank=True, related_name='+')

    def __str__(self):
        return self.name + " " + self.creator.get_full_name()

    class Meta:
        verbose_name = "плейлист"
        verbose_name_plural = "плейлисты"
        ordering = ['order']

    @receiver(post_save, sender=Community)
    def create_c_model(sender, instance, created, **kwargs):
        if created:
            SoundList.objects.create(community=instance, type=SoundList.MAIN, name="Основной список", order=0, creator=instance.creator)
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_u_model(sender, instance, created, **kwargs):
        if created:
            SoundList.objects.create(creator=instance, type=SoundList.MAIN, name="Основной список", order=0)

    def is_item_in_list(self, item_id):
        return self.playlist.filter(pk=item_id).values("pk").exists()

    def is_not_empty(self):
        return self.playlist.filter(Q(status="PUB")|Q(status="PRI")).values("pk").exists()

    def get_staff_items(self):
        return self.playlist.filter(Q(status="PUB")|Q(status="PRI"))
    def get_items(self):
        return self.playlist.filter(status="PUB")
    def get_6_items(self):
        return self.playlist.filter(status="PUB")[:6]
    def get_manager_items(self):
        return self.playlist.filter(status="MAN")
    def count_items(self):
        return self.playlist.filter(Q(status="PUB")|Q(status="PRI")).values("pk").count()

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
    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type[0] == "_"

    @classmethod
    def create_list(cls, creator, name, description, order, community, is_public):
        from notify.models import Notify, Wall
        from common.processing.music import get_playlist_processing
        if not order:
            order = 1
        if community:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order, community=community)
            if is_public:
                from common.notify.progs import community_send_notify, community_send_wall
                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="MUL", object_id=list.pk, verb="ITE")
                community_send_wall(list.pk, creator.pk, community.pk, None, "create_c_music_list_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="MUL", object_id=list.pk, verb="ITE")
                    community_send_notify(list.pk, creator.pk, user_id, community.pk, None, "create_c_music_list_notify")
        else:
            list = cls.objects.create(creator=creator,name=name,description=description, order=order)
            if is_public:
                from common.notify.progs import user_send_notify, user_send_wall
                Wall.objects.create(creator_id=creator.pk, type="MUL", object_id=list.pk, verb="ITE")
                user_send_wall(list.pk, None, "create_u_music_list_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="MUL", object_id=list.pk, verb="ITE")
                    user_send_notify(list.pk, creator.pk, user_id, None, "create_u_music_list_notify")
        get_playlist_processing(list, SoundList.LIST)
        return list

    def edit_list(self, name, description, order, is_public):
        from common.processing.music import get_playlist_processing

        if not order:
            order = 1
        self.name = name
        self.description = description
        self.order = order
        self.save()
        if is_public:
            get_playlist_processing(self, SoundList.LIST)
            self.make_publish()
        else:
            get_playlist_processing(self, SoundList.PRIVATE)
            self.make_private()
        return self

    def make_private(self):
        from notify.models import Notify, Wall
        self.type = SoundList.PRIVATE
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.type = SoundList.LIST
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")

    def delete_list(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SoundList.THIS_DELETED
        elif self.type == "PRI":
            self.type = SoundList.THIS_DELETED_PRIVATE
        elif self.type == "MAN":
            self.type = SoundList.THIS_DELETED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="C")
    def restore_list(self):
        from notify.models import Notify, Wall
        if self.type == "_DEL":
            self.type = SoundList.LIST
        elif self.type == "_DELP":
            self.type = SoundList.PRIVATE
        elif self.type == "_DELM":
            self.type = SoundList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUL", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self):
        from notify.models import Notify, Wall
        if self.type == "LIS":
            self.type = SoundList.THIS_CLOSED
        elif self.type == "MAI":
            self.type = SoundList.THIS_CLOSED_MAIN
        elif self.type == "PRI":
            self.type = SoundList.THIS_CLOSED_PRIVATE
        elif self.type == "MAN":
            self.type = SoundList.THIS_CLOSED_MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self):
        from notify.models import Notify, Wall
        if self.type == "_CLO":
            self.type = SoundList.LIST
        elif self.type == "_CLOM":
            self.type = SoundList.MAIN
        elif self.type == "_CLOP":
            self.type = SoundList.PRIVATE
        elif self.type == "_CLOM":
            self.type = SoundList.MANAGER
        self.save(update_fields=['type'])
        if Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="DOL", object_id=self.pk, verb="ITE").update(status="R")

    @classmethod
    def get_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_user_staff_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_user_lists(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_user_lists_count(cls, user_pk):
        query = Q(creator_id=user_pk, community__isnull=True)|Q(users__id=user_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()

    @classmethod
    def get_community_staff_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query)
    @classmethod
    def is_have_community_staff_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(~Q(Q(type__contains="_")|Q(type="MAI")), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).order_by("order")
    @classmethod
    def is_have_community_lists(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).exists()
    @classmethod
    def get_community_lists_count(cls, community_pk):
        query = Q(community_id=user_pk)|Q(communities__id=community_pk)
        query.add(Q(type="LIS"), Q.AND)
        return cls.objects.filter(query).values("pk").count()


class SoundTags(models.Model):
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=0)
    symbol = models.ForeignKey(SoundSymbol, related_name="symbol_papa", on_delete=models.CASCADE, verbose_name="Буква")

    def __str__(self):
        return self.name

    def is_track_in_tag(self, track_id):
        self.track_tag.filter(id=track_id).exists()

    def get_genres(self):
        from django.db.models import Q

        genres_list = []
        genres = self.track_tag.values('genre_id')
        genres_ids = [id['genre_id'] for id in genres]
        for genre in genres_ids:
            if not genre in genres_list:
                genres_list = genres_list + [genre,]

        genres_query = Q(id__in=genres_list)
        result = SoundGenres.objects.filter(genres_query)
        return result

    def get_items(self):
        queryset = self.track_tag.all()
        return queryset

    def get_tracks_count(self):
        return self.track_tag.count()

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

class UserTempSoundList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_of_field', db_index=False, on_delete=models.CASCADE, verbose_name="Слушатель")
    list = models.ForeignKey(SoundList, related_name='list_field', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Связь на плейлист человека или сообщества")
    tag = models.ForeignKey(SoundTags, related_name='tag_field', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Связь на тег")
    genre = models.ForeignKey(SoundGenres, related_name='genre_field', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Связь на жанр")


class Music(models.Model):
    THIS_PROCESSING, PUBLISHED, PRIVATE, MANAGER, THIS_DELETED, THIS_CLOSED = '_PRO','PUB','PRI','MAN','_DEL','_CLO'
    THIS_DELETED_PRIVATE, THIS_DELETED_MANAGER, THIS_CLOSED_PRIVATE, THIS_CLOSED_MANAGER = '_DELP','_DELM','_CLOP','_CLOM'
    STATUS = (
        (THIS_PROCESSING, 'Обработка'),(PUBLISHED, 'Опубликовано'),(THIS_DELETED, 'Удалено'),(PRIVATE, 'Приватно'),(THIS_CLOSED, 'Закрыто модератором'),(MANAGER, 'Созданный персоналом'),
        (THIS_DELETED_PRIVATE, 'Удалённый приватный'),(THIS_DELETED_MANAGER, 'Удалённый менеджерский'),(THIS_CLOSED_PRIVATE, 'Закрытый приватный'),(THIS_CLOSED_MANAGER, 'Закрытый менеджерский'),
    )
    image = ProcessedImageField(format='JPEG', blank=True, options={'quality': 100}, upload_to=upload_to_music_directory, processors=[Transpose(), ResizeToFit(width=100, height=100)])
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    duration = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    genre = models.ForeignKey(SoundGenres, related_name='track_genre', on_delete=models.CASCADE, verbose_name="Жанр трека")
    tag = models.ForeignKey(SoundTags, blank=True, null=True, related_name='track_tag', on_delete=models.CASCADE, verbose_name="Буква")
    title = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    list = models.ManyToManyField(SoundList, related_name='playlist', blank="True")
    status = models.CharField(choices=STATUS, default=THIS_PROCESSING, max_length=5)
    file = models.FileField(upload_to=upload_to_music_directory, blank=True, validators=[validate_file_extension], verbose_name="Аудиозапись")
    community = models.ForeignKey('communities.Community', related_name='music_community', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")

    view = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    like = models.PositiveIntegerField(default=0, verbose_name="Кол-во лайков")
    dislike = models.PositiveIntegerField(default=0, verbose_name="Кол-во дизлайков")
    repost = models.PositiveIntegerField(default=0, verbose_name="Кол-во репостов")

    class Meta:
        verbose_name = "спарсенные треки"
        verbose_name_plural = "спарсенные треки"
        indexes = (BrinIndex(fields=['created']),)
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_mp3(self):
        url = self.uri + '/stream?client_id=3ddce5652caa1b66331903493735ddd64d'
        url.replace("\\?", "%3f")
        url.replace("=", "%3d")
        return url
    def get_uri(self):
        if self.file:
            return self.file.url
        else:
            return self.uri

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

    @classmethod
    def create_track(cls, creator, title, file, lists, is_public, community):
        from common.processing.music import get_music_processing

        if not lists:
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Не выбран список для нового документа")
        private = 0
        track = cls.objects.create(creator=creator,title=title,file=file)
        if community:
            community.plus_tracks(1)
        else:
            user.plus_tracks(1)
        for list_id in lists:
            track_list = SoundList.objects.get(pk=list_id)
            track_list.playlist.add(track)
            if track_list.is_private():
                private = 1
        if not private and is_public:
            get_music_processing(track, Track.PUBLISHED)
            if community:
                from common.notify.progs import community_send_notify, community_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="MUS", object_id=track.pk, verb="ITE")
                community_send_wall(track.pk, creator.pk, community.pk, None, "create_c_track_wall")
                for user_id in community.get_member_for_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, community_id=community.pk, recipient_id=user_id, type="MUS", object_id=track.pk, verb="ITE")
                    community_send_notify(track.pk, creator.pk, user_id, community.pk, None, "create_c_track_notify")
            else:
                from common.notify.progs import user_send_notify, user_send_wall
                from notify.models import Notify, Wall

                Wall.objects.create(creator_id=creator.pk, type="MUS", object_id=track.pk, verb="ITE")
                user_send_wall(track.pk, None, "create_u_track_wall")
                for user_id in creator.get_user_news_notify_ids():
                    Notify.objects.create(creator_id=creator.pk, recipient_id=user_id, type="MUS", object_id=track.pk, verb="ITE")
                    user_send_notify(track.pk, creator.pk, user_id, None, "create_u_track_notify")
        else:
            get_music_processing(track, Music.PRIVATE)
        return track

    def edit_track(self, title, file, lists, is_public):
        from common.processing.music  import get_music_processing

        self.title = title
        self.file = file
        self.lists = lists
        if is_public:
            get_music_processing(self, Music.PUBLISHED)
            self.make_publish()
        else:
            get_music_processing(self, Music.PRIVATE)
            self.make_private()
        return self.save()

    def delete_track(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Music.THIS_DELETED
        elif self.status == "PRI":
            self.status = Music.THIS_DELETED_PRIVATE
        elif self.status == "MAN":
            self.status = Music.THIS_DELETED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_tracks(1)
        else:
            self.creator.minus_tracks(1)
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def restore_track(self, community):
        from notify.models import Notify, Wall
        if self.status == "_DEL":
            self.status = Music.PUBLISHED
        elif self.status == "_DELP":
            self.status = Music.PRIVATE
        elif self.status == "_DELM":
            self.status = Music.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_tracks(1)
        else:
            self.creator.plus_tracks(1)
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def close_item(self, community):
        from notify.models import Notify, Wall
        if self.status == "PUB":
            self.status = Music.THIS_CLOSED
        elif self.status == "PRI":
            self.status = Music.THIS_CLOSED_PRIVATE
        elif self.status == "MAN":
            self.status = Music.THIS_CLOSED_MANAGER
        self.save(update_fields=['status'])
        if community:
            community.minus_tracks(1)
        else:
            self.creator.minus_tracks(1)
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def abort_close_item(self, community):
        from notify.models import Notify, Wall
        if self.status == "_CLO":
            self.status = Music.PUBLISHED
        elif self.status == "_CLOP":
            self.status = Music.PRIVATE
        elif self.status == "_CLOM":
            self.status = Music.MANAGER
        self.save(update_fields=['status'])
        if community:
            community.plus_tracks(1)
        else:
            self.creator.plus_tracks(1)
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def make_private(self):
        from notify.models import Notify, Wall
        self.status = Music.PRIVATE
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="C")
    def make_publish(self):
        from notify.models import Notify, Wall
        self.status = Music.PUBLISHED
        self.save(update_fields=['status'])
        if Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Notify.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")
        if Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").exists():
            Wall.objects.filter(type="MUS", object_id=self.pk, verb="ITE").update(status="R")

    def is_private(self):
        return self.type == self.PRIVATE
    def is_open(self):
        return self.type == self.MANAGER or self.type == self.PUBLISHED

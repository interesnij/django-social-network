import soundcloud
from django.conf import settings
from django.db import models
from common.utils import safe_json
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.indexes import BrinIndex


class SoundGenres(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="жанр"
        verbose_name_plural="жанры"


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
        verbose_name="буква поиска музыки"
        verbose_name_plural="буквы поиска музыки"


class SoundList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    track = models.ManyToManyField('music.SoundParsing', related_name='players', blank="True")
    community = models.ForeignKey('communities.Community', related_name='community_playlist', db_index=False, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Сообщество")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_playlist', db_index=False, on_delete=models.CASCADE, verbose_name="Создатель")

    def __str__(self):
        return self.name

    def is_track_in_list(self, track_id):
        self.track.filter(id=track_id).exists()

    def get_json_playlist(self):
        if not hasattr(self, '_cached_playlist'):
            self._cached_playlist = safe_json(self.playlist())
        return self._cached_playlist

    def playlist(self):
        playlist = []
        queryset = self.track.all()
        for track in queryset:
            url = track.uri + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d'
            genre = str(track.genre)
            data = {}
            data['title'] = track.title
            data['artwork_url'] = track.artwork_url
            data['mp3'] = url
            data['genre'] = genre
            if self.is_track_in_list(track.pk):
                data['is_my_track'] = 1
            else:
                data['is_my_track'] = 0
            data['pk'] = track.pk
            playlist.append(data)
        return playlist

    class Meta:
        verbose_name="список: весь, человека или сообщества"
        verbose_name_plural="списки: весь, человека или сообщества"


class SoundTags(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    order = models.IntegerField(default=0)
    symbol = models.ForeignKey(SoundSymbol, related_name="symbol_papa", on_delete=models.CASCADE, verbose_name="Буква")

    def __str__(self):
        return self.name

    def is_track_in_tag(self, track_id):
        self.track_tag.filter(id=track_id).exists()

    def get_genres(self):
        genres_list = []
        genres = self.soundparsing_set.all().values('genre_id')
        genres_ids = [id['genre_id'] for id in genres]
        for genre in genres_ids:
            if not genre in genres_list:
                genres_list = genres_list + [genre,]

        genres_query = Q(id__in=genres_list)
        result = SoundGenres.objects.filter(genres_query)
        return result

    def get_json_playlist(self):
        if not hasattr(self, '_cached_playlist'):
            self._cached_playlist = safe_json(self.playlist())
        return self._cached_playlist

    def playlist(self):
        playlist = []
        queryset = self.soundparsing_set.all()
        for track in queryset:
            url = track.uri + '/stream?client_id=' + 'dce5652caa1b66331903493735ddd64d'
            genre = str(track.genre)
            data = {}
            data['title'] = track.title
            data['artwork_url'] = track.artwork_url
            data['mp3'] = url
            data['genre'] = genre
            data['pk'] = track.pk
            if self.is_track_in_tag(track.pk):
                data['is_my_track'] = 1
            else:
                data['is_my_track'] = 0
            playlist.append(data)
        return playlist

    class Meta:
        verbose_name="тег"
        verbose_name_plural="теги"

class UserTempSoundList(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, db_index=False, on_delete=models.CASCADE, verbose_name="Слушатель")
    tag = models.OneToOneField(SoundTags, related_name='tag_field', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Связь на тег")
    list = models.OneToOneField(SoundList, related_name='list_field', null=True, blank=True, on_delete=models.CASCADE, verbose_name="Связь на плейлист человека или сообщества")

    def __str__(self):
        return self.user.get_full_name()


class SoundParsing(models.Model):
    moderated_object = GenericRelation('moderation.ModeratedObject', related_query_name='music')
    id = models.IntegerField(primary_key=True)
    artwork_url = models.URLField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    genre = models.ForeignKey(SoundGenres, on_delete=models.CASCADE, verbose_name="Жанр трека")
    permalink = models.CharField(max_length=100, blank=True, null=True)
    stream_url = models.URLField(max_length=1000, blank=True, null=True)
    tag = models.ForeignKey(SoundTags, related_name='track_tag', on_delete=models.CASCADE, verbose_name="Буква")
    title = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(verbose_name="Удален",default=False )


    def __str__(self):
        return self.title

    class Meta:
        verbose_name="спарсенные треки"
        verbose_name_plural="спарсенные треки"
        indexes = (BrinIndex(fields=['created_at']),)

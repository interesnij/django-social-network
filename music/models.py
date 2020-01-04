import soundcloud
from django.conf import settings
from django.db import models
from common.utils import safe_json
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class Playlist(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    track = models.ManyToManyField('music.SoundParsing', related_name='players', blank="True")
    autoplay = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_json_playlist(self):
        if not hasattr(self, '_cached_playlist'):
            self._cached_playlist = safe_json(self.playlist())
        return self._cached_playlist

    def playlist(self):
        playlist = []
        queryset = self.track.all()
        for track in queryset:
            data = {}
            data['title'] = track.title
            data['artwork_url'] = track.artwork_url
            data['mp3'] = track.stream_url
            data['author'] = "Винни Пух"
            playlist.append(data)
        return playlist

    def get_base_path(self):
        return safe_json(settings.JPLAYER_BASE_PATH)

    def get_json_autoplay(self):
        return safe_json(self.autoplay)


class SounGenres(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class SoundParsing(models.Model):
    id = models.IntegerField(primary_key=True)
    artwork_url = models.URLField(max_length=255, blank=True, null=True)
    bpm = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    genre = models.ForeignKey(SounGenres, on_delete=models.CASCADE, verbose_name="Жанр трека")
    permalink = models.CharField(max_length=100, blank=True, null=True)
    stream_url = models.URLField(max_length=1000, blank=True, null=True)
    streamable = models.BooleanField(default=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)

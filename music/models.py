from django.db import models


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
    permalink = models.CharField(max_length=255, blank=True, null=True)
    release_day = models.CharField(max_length=255, blank=True, null=True)
    release_month = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.CharField(max_length=255, blank=True, null=True)
    stream_url = models.URLField(max_length=255, blank=True, null=True)
    streamable = models.BooleanField(default=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)

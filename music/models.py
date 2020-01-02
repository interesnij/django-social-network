from django.db import models


class SoundParsing(models.Model):
    artwork_url = models.URLField(max_length=255, blank=True, null=True)
    bpm = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=255, blank=True, null=True)
    permalink = models.CharField(max_length=255, blank=True, null=True)
    permalink_url = models.URLField(max_length=255, blank=True, null=True)
    release = models.CharField(max_length=255, blank=True, null=True)
    release_day = models.CharField(max_length=255, blank=True, null=True)
    release_month = models.CharField(max_length=255, blank=True, null=True)
    release_year = models.CharField(max_length=255, blank=True, null=True)
    stream_url = models.URLField(max_length=255, blank=True, null=True)
    streamable = models.BooleanField(default=True, null=True)
    tag_list = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    uri = models.CharField(max_length=255, blank=True, null=True)
    isrc = models.CharField(max_length=255, blank=True, null=True)
    label_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)

from music.models import *
from users.models import User
from django.http import HttpResponse
from django.views import View
from rest_framework.exceptions import PermissionDenied


class TempListOn(View):
    """
    Выставляем плейлист пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        list = SoundList.objects.get(pk=self.kwargs["pk"])
        try:
            my_list = UserTempSoundList.objects.get(user=request.user)
        except:
            my_list = UserTempSoundList.objects.create(user=request.user)
        my_list.tag = None
        my_list.genre = None
        my_list.save()
        return HttpResponse("!")


class TempTagOn(View):
    """
    Выставляем поисковый тег (исполнителя) для пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        tag = SoundTags.objects.get(pk=self.kwargs["pk"])
        try:
            temp_tag = UserTempSoundList.objects.get(user=request.user)
        except:
            temp_tag = UserTempSoundList.objects.create(user=request.user)
        temp_tag.list = None
        temp_tag.genre = None
        temp_tag.tag = tag
        temp_tag.save()
        return HttpResponse("!")


class TempGenreOn(View):
    """
    Выставляем плейлист жанра как активный.
    """
    def get(self, request, *args, **kwargs):
        genre = SoundGenres.objects.get(pk=self.kwargs["pk"])
        try:
            temp_genre = UserTempSoundList.objects.get(user=request.user)
        except:
            temp_genre = UserTempSoundList.objects.create(user=request.user)
        temp_genre.list = None
        temp_genre.genre = genre
        temp_genre.tag = None
        temp_genre.save()
        return HttpResponse("!")


class TrackAdd(View):
    """
    Добавляем трек в свой плейлист, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        my_list = SoundList.objects.get(creator_id=request.user.pk, community=None, is_generic=True)
        if not my_list.is_track_in_list(track.pk):
            my_list.track.add(track)
        return HttpResponse("!") 

class TrackRemove(View):
    """
    Удаляем трек из своего плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        my_list = SoundList.objects.get(creator_id=request.user.pk, community=None, is_generic=True)
        if my_list.is_track_in_list(track.pk):
            my_list.track.remove(track)
        return HttpResponse("!")

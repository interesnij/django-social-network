from music.models import *
from users.models import User
from django.http import HttpResponse
from django.views import View
from rest_framework.exceptions import PermissionDenied


class TempListOn(View):
    """
    Выставляем плейлист человека или сообщества для пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        self.list=SoundList.objects.get(pk=self.kwargs["pk"])
        if self.list.is_temp_list(user=request.user):
            HttpResponse("!")
        temp_list = UserTempSoundList.objects.get(user=request.user)
        temp_list.list = self.list
        temp_list.tag = None
        temp_list.save()
        return HttpResponse("!")

class TempTagOn(View):
    """
    Выставляем поисковый тег (исполнителя) для пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        self.tag=SoundTags.objects.get(pk=self.kwargs["pk"])
        if self.tag.is_temp_tag(user=request.user):
            HttpResponse("!")
        temp_tag = UserTempSoundList.objects.get(user=request.user)
        temp_tag.list = None
        temp_tag.tag = self.tag
        temp_tag.save()
        return HttpResponse("!")

class MyListOn(View):
    """
    Выставляем собственный плейлист пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        my_list = UserTempSoundList.objects.get(user=request.user)
        my_list.list = None
        my_list.tag = None
        my_list.save()
        return HttpResponse("!")

class TrackAdd(View):
    """
    Добавляем трек в свой плейлист, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = SoundParsing.objects.get(pk=self.kwargs["pk"])
        my_list = SoundList.objects.get(creator_id=self.id, name="my_first_generic_playlist_number_12345678900000000")
        if not request.user.is_track_exists(track.pk):
            my_list.add(track)
        return HttpResponse("!")

class TrackRemove(View):
    """
    Удаляем трек из своего плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundParsing.objects.get(pk=self.kwargs["pk"])
        my_list = SoundList.objects.get(creator_id=self.id, name="my_first_generic_playlist_number_12345678900000000")
        if not request.user.is_track_exists(track.pk):
            my_list.remove(track)
        return HttpResponse("!")

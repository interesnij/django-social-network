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
        list = SoundList.objects.get(pk=self.kwargs["pk"])
        temp_list = UserTempSoundList.objects.get(user=request.user)
        temp_list.list = list
        temp_list.tag = None
        temp_list.save()
        return HttpResponse("!")

class TempTagOn(View):
    """
    Выставляем поисковый тег (исполнителя) для пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        tag = SoundTags.objects.get(pk=self.kwargs["pk"])
        temp_tag = UserTempSoundList.objects.get(user=request.user)
        temp_tag.list = None
        temp_tag.tag = tag
        temp_tag.save()
        return HttpResponse("!")

class MyListOn(View):
    """
    Выставляем собственный плейлист пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        my_list = UserTempSoundList.objects.get(user=user)
        my_list.list = None
        my_list.tag = None
        my_list.save()
        return HttpResponse("!")

class TrackAdd(View):
    """
    Добавляем трек в свой плейлист, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        my_list = SoundList.objects.get(creator_id=request.user.pk, name="my_first_generic_playlist_number_12345678900000000")
        if not my_list.is_track_in_list(track.pk):
            my_list.track.add(track)
        return HttpResponse("!")

class TrackRemove(View):
    """
    Удаляем трек из своего плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        my_list = SoundList.objects.get(creator_id=request.user.pk, name="my_first_generic_playlist_number_12345678900000000")
        if not my_list.is_track_in_list(track.pk):
            my_list.track.remove(track)
        return HttpResponse("!")

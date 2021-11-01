from music.models import *
from users.models import User
from django.views import View
from rest_framework.exceptions import PermissionDenied
from music.forms import PlaylistForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.templates import render_for_platform


class TempListOn(View):
    """
    Выставляем плейлист пользователя как активный.
    """
    def get(self, request, *args, **kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
        try:
            my_list = UserTempMusicList.objects.get(user=request.user)
        except:
            my_list = UserTempMusicList.objects.create(user=request.user)
        if request.is_ajax():
            my_list.tag = None
            my_list.genre = None
            my_list.list = list
            my_list.save()
            return HttpResponse()
        else:
            raise Http404

class TempGenreOn(View):
    """
    Выставляем плейлист жанра как активный.
    """
    def get(self, request, *args, **kwargs):
        genre = SoundGenres.objects.get(pk=self.kwargs["pk"])
        try:
            temp_genre = UserTempMusicList.objects.get(user=request.user)
        except:
            temp_genre = UserTempMusicList.objects.create(user=request.user)
        if request.is_ajax():
            temp_genre.list = None
            temp_genre.genre = genre
            temp_genre.tag = None
            temp_genre.save()
            return HttpResponse()
        else:
            raise Http404

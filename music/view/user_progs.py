from music.models import *
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import PlaylistForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from common.parsing_soundcloud.add_playlist import add_playlist


class UserSoundcloudSetPlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="music_create/", template="soundcloud_add_playlist.html", request=request)
        return super(UserSoundcloudSetPlaylistWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetPlaylistWindow,self).get_context_data(**kwargs)
        context['form_post'] = PlaylistForm()
        return context

class UserSoundcloudSetMainWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="music_create/", template="soundcloud_set_playlist_main.html", request=request)
        return super(UserSoundcloudSetMainWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetMainWindow,self).get_context_data(**kwargs)
        return context

class UserSoundcloudSetWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="music_create/", template="soundcloud_set_playlist.html", request=request)
        return super(UserSoundcloudSetWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetWindow,self).get_context_data(**kwargs)
        return context


class UserSoundcloudSetCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = PlaylistForm(request.POST)
        user = User.objects.get(pk=self.kwargs["pk"])

        if form_post.is_valid() and request.user == user:
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            new_list.save()
            add_playlist(request.POST.get('permalink'), request.user, new_list)
            return render(request, 'user_music_list/my_list.html',{'playlist': new_list, 'object_list': new_list.playlist_too(),'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserSoundcloudSetMain(View):
    def post(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.user == user:
            add_playlist(request.POST.get('permalink'), request.user, list)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
class UserSoundcloudSet(View):
    def post(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.user == user:
            add_playlist(request.POST.get('permalink'), request.user, list)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class UserTrackAdd(View):
    """
    Добавляем трек в свой плейлист, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        try:
            my_list = SoundList.objects.get(creator_id=request.user.pk, community=None, is_generic=True)
        except:
            my_list = SoundList.objects.create(creator_id=request.user.pk, community=None, is_generic=True, name="Основной плейлист")
        if not my_list.is_track_in_list(track.pk):
            my_list.players.add(track)
        return HttpResponse("!")

class UserTrackRemove(View):
    """
    Удаляем трек из своего плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        my_list = SoundList.objects.get(creator_id=request.user.pk, community=None, is_generic=True)
        if my_list.is_track_in_list(track.pk):
            my_list.players.remove(track)
        return HttpResponse("!")

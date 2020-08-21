from music.models import *
from community.models import Community
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import PlaylistForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from common.parsing_soundcloud.add_playlist import add_playlist
from django.http import Http404


class CommunitySoundcloudSetPlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="music_create/", template="c_soundcloud_add_playlist.html", request=request)
        return super(CommunitySoundcloudSetPlaylistWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunitySoundcloudSetPlaylistWindow,self).get_context_data(**kwargs)
        context['form_post'] = PlaylistForm()
        return context

class CommunitySoundcloudSetWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="music_create/", template="c_soundcloud_set_playlist.html", request=request)
        return super(CommunitySoundcloudSetWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunitySoundcloudSetWindow,self).get_context_data(**kwargs)
        return context


class CommunitySoundcloudSetCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(CommunitySoundcloudSetCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = PlaylistForm(request.POST)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            new_list.community = community
            new_list.save()
            add_playlist(request.POST.get('permalink'), request.user, new_list)
            return render(request, 'community_music_list/my_list.html',{'playlist': new_list, 'object_list': new_list.playlist_too(),'community': community})
        else:
            return HttpResponseBadRequest()

class CommunitySoundcloudSet(View):
    def post(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community_with_name(community.name):
            add_playlist(request.POST.get('permalink'), request.user, list)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class CommunityTrackAdd(View):
    """
    Добавляем трек в плейлист сообщества, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_track_in_list(track.pk) and request.user.is_staff_of_community_with_name(list.community.name):
            list.players.add(track)
            return HttpResponse()
        else:
            raise Http404

class CommunityTrackRemove(View):
    """
    Удаляем трек из плейлиста сообщества, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_track_in_list(track.pk) and request.user.is_staff_of_community_with_name(list.community.name):
            list.players.remove(track)
            return HttpResponse()
        else:
            raise Http404

class CommunityTrackListAdd(View):
    """
    Добавляем трек в любой плейлист сообщества, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_track_in_list(track.pk) and request.user.is_staff_of_community_with_name(list.community.name):
            list.players.add(track)
            return HttpResponse()
        else:
            raise Http404

class CommunityTrackListRemove(View):
    """
    Удаляем трек из любого плейлиста сообщества, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_track_in_list(track.pk) and request.user.is_staff_of_community_with_name(list.community.name):
            list.players.remove(track)
            return HttpResponse()
        else:
            raise Http404

class CommunityCreatePlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.user.get_settings_template(folder="music_create/", template="c_create_list.html", request=request)
        return super(CommunityCreatePlaylistWindow,self).get(request,*args,**kwargs)

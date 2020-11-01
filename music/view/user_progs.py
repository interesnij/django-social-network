from music.models import *
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import PlaylistForm
from django.http import HttpResponse, HttpResponseBadRequest
from common.parsing_soundcloud.add_playlist import add_playlist
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform


class UserSoundcloudSetPlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("music/music_create/u_soundcloud_add_playlist.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserSoundcloudSetPlaylistWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetPlaylistWindow,self).get_context_data(**kwargs)
        context['form_post'] = PlaylistForm()
        return context

class UserSoundcloudSetWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("music/music_create/u_soundcloud_set_playlist.html", request.user, request.META['HTTP_USER_AGENT'])
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

        if request.is_ajax() and form_post.is_valid() and request.user == user:
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            new_list.save()
            add_playlist(request.POST.get('permalink'), request.user, new_list)
            return render_for_platform(request, 'users/user_music_list/my_list.html',{'playlist': new_list, 'object_list': new_list.playlist_too(),'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserSoundcloudSet(View):
    def post(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user == user:
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
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_track_in_list(track.pk):
            list.players.add(track)
            return HttpResponse()
        else:
            raise Http404

class UserTrackRemove(View):
    """
    Удаляем трек из своего плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_track_in_list(track.pk):
            list.players.remove(track)
            return HttpResponse()
        else:
            raise Http404

class UserTrackListAdd(View):
    """
    Добавляем трек в любой плейлист, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_track_in_list(track.pk):
            list.players.add(track)
            return HttpResponse()
        else:
            raise Http404

class UserTrackListRemove(View):
    """
    Удаляем трек из любого плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_track_in_list(track.pk):
            list.players.remove(track)
            return HttpResponse()
        else:
            raise Http404

class UserCreatePlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("music/music_create/u_create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCreatePlaylistWindow,self).get(request,*args,**kwargs)

class UserEditPlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_settings_template("music/music_create/u_edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserEditPlaylistWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserEditPlaylistWindow,self).get_context_data(**kwargs)
        context["playlist"] = self.playlist
        return context


class UserPlaylistCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserPlaylistCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = PlaylistForm(request.POST)
        user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user == user:
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            if not new_list.order:
                new_list.order = 0
            new_list.save()
            return render_for_platform(request, 'users/user_music_list/my_list.html',{'playlist': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserPlaylistEdit(TemplateView):
    """
    изменение плейлиста пользователя
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("music/music_create/u_edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPlaylistEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["list"] = SoundList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PlaylistForm(request.POST,instance=self.list)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

class UserPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user and list.type == SoundList.LIST:
            list.is_deleted = True
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserPlaylistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and user == request.user:
            list.is_deleted = False
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

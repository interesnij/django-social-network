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
from common.check.user import check_user_can_get_list


class UserSoundcloudSetPlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("music/music_create/u_soundcloud_add_playlist.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserSoundcloudSetPlaylistWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetPlaylistWindow,self).get_context_data(**kwargs)
        context['form_post'] = PlaylistForm()
        return context

class UserSoundcloudSetWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
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

        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = SoundList.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=None, is_public=request.POST.get("is_public"))
            add_playlist(request.POST.get('permalink'), request.user, new_list)
            return render_for_platform(request, 'users/user_music_list/my_list.html',{'playlist': new_list, 'object_list': new_list.get_items(),'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserSoundcloudSet(View):
    def post(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            add_playlist(request.POST.get('permalink'), request.user, list)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class AddPlayListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.users.add(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemovePlayListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.users.remove(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class UserTrackAdd(View):
    """
    Добавляем трек в свой плейлист, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_track_in_list(track.pk):
            list.playlist.add(track)
            return HttpResponse()
        else:
            raise Http404

class UserTrackRemove(View):
    """
    Удаляем трек из своего плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_track_in_list(track.pk):
            list.playlist.remove(track)
            return HttpResponse()
        else:
            raise Http404

class UserTrackListAdd(View):
    """
    Добавляем трек в любой плейлист, если его там нет
    """
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_track_in_list(track.pk):
            list.playlist.add(track)
            return HttpResponse()
        else:
            raise Http404

class UserTrackListRemove(View):
    """
    Удаляем трек из любого плейлиста, если он там есть
    """
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_track_in_list(track.pk):
            list.playlist.remove(track)
            return HttpResponse()
        else:
            raise Http404

class UserCreatePlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("music/music_create/u_create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCreatePlaylistWindow,self).get(request,*args,**kwargs)

class UserEditPlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
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

        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=None,is_public=request.POST.get("is_public"))
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
        self.user = request.user
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
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            new_list = list.create_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

class UserPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.type == SoundList.LIST:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class UserPlaylistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            list.abort_delete_list()
            return HttpResponse()
        else:
            raise Http404

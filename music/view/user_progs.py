from music.models import *
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import PlaylistForm, TrackForm
from django.http import HttpResponse, HttpResponseBadRequest
from common.parsing_soundcloud.add_playlist import add_playlist
from django.http import Http404
from common.templates import get_settings_template, render_for_platform
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
        self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_settings_template("music/music_create/u_soundcloud_set_playlist.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserSoundcloudSetWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSoundcloudSetWindow,self).get_context_data(**kwargs)
        context["list"] = self.list
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
            new_list = SoundList.create_list(creator=request.user, name=list.name, description=list.description, community=None)
            add_playlist(request.POST.get('permalink'), request.user, new_list)
            return render_for_platform(request, 'users/music/list/my_list.html',{'playlist': new_list, 'object_list': new_list.get_items(),'user': request.user})
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
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemovePlayListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class AddTrackInUserList(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_item_in_list(track.pk):
            list.playlist.add(track)
            return HttpResponse()
        else:
            raise Http404

class RemoveTrackFromUserList(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(track.pk):
            list.playlist.remove(track)
            return HttpResponse()
        else:
            raise Http404


class UserPlaylistCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("music/music_create/u_create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPlaylistCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPlaylistCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = PlaylistForm(request.POST)

        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=None)
            return render_for_platform(request, 'users/music/list/my_list.html',{'playlist': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserPlaylistEdit(TemplateView):
    """
    изменение плейлиста пользователя
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("music/music_create/u_edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserPlaylistEdit,self).get_context_data(**kwargs)
        context["list"] = SoundList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PlaylistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            new_list = list.edit_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

class UserPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.type != SoundList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserPlaylistRecover(View):
    def get(self,request,*args,**kwargs):
        list = SoundList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class UserTrackRemove(View):
    def get(self, request, *args, **kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and track.creator.pk == request.user.pk:
            track.delete_track(None)
            return HttpResponse()
        else:
            raise Http404
class UserTrackAbortRemove(View):
    def get(self,request,*args,**kwargs):
        track = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and track.creator == request.user:
            track.restore_track(None)
            return HttpResponse()
        else:
            raise Http404

class UserTrackCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("music/music_create/u_create_track.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserTrackCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserTrackCreate,self).get_context_data(**kwargs)
        context["form_post"] = TrackForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = TrackForm(request.POST, request.FILES)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid():
            track = form_post.save(commit=False)
            new_track = Music.create_track(creator=request.user, title=track.title, file=track.file, list=track.list, is_public=request.POST.get("is_public"), community=None)
            return render_for_platform(request, 'music/music_create/u_new_track.html',{'object': new_track})
        else:
            return HttpResponseBadRequest()

class UserTrackEdit(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("music/music_create/u_edit_track.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserTrackEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserTrackEdit,self).get_context_data(**kwargs)
        context["form_post"] = TrackForm(instance=self.track)
        context["track"] = self.track
        return context

    def post(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["pk"])
        form_post = TrackForm(request.POST, request.FILES, instance=self.track)

        if request.is_ajax() and form_post.is_valid():
            _track = form_post.save(commit=False)
            new_doc = self.track.edit_track(title=_track.title, file=_track.file, lists=request.POST.getlist("list"), is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'music/music_create/u_new_track.html',{'object': self.track})
        else:
            return HttpResponseBadRequest()


class UserChangeMusicPosition(View):
    def post(self,request,*args,**kwargs):
        import json

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                post = Music.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class UserChangeMusicListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from users.model.list import UserPlayListPosition

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                list = UserPlayListPosition.objects.get(list=item['key'], user=user.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()

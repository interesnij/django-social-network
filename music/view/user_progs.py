from music.models import *
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import PlaylistForm, TrackForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.templates import get_settings_template, render_for_platform
from common.check.user import check_user_can_get_list



class AddPlayListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemovePlayListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

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
            new_list = list.create_list(
                creator=request.user,
                name=list.name,
                description=list.description,
                community=None,
                can_see_el=list.can_see_el,
                can_see_el_users=request.POST.getlist("can_see_el_users"),
                create_el=list.create_el,
                create_el_users=request.POST.getlist("create_el_users"),
                copy_el=list.copy_el,
                copy_el_users=request.POST.getlist("create_copy_el"),)
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
        context["list"] = MusicList.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = MusicList.objects.get(pk=self.kwargs["pk"])
        self.form = PlaylistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid():
            list = self.form.save(commit=False)
            new_list = list.edit_list(
                name=list.name,
                description=list.description,
                can_see_el=list.can_see_el,
                can_see_el_users=request.POST.getlist("can_see_el_users"),
                create_el=list.create_el,
                create_el_users=request.POST.getlist("create_el_users"),
                copy_el=list.copy_el,
                copy_el_users=request.POST.getlist("copy_el_users"),)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserPlaylistEdit,self).get(request,*args,**kwargs)

class UserPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.type != MusicList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserPlaylistRecover(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
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
            new_track = Music.create_track(creator=request.user, title=track.title, file=track.file, list=track.list)
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
            new_doc = self.track.edit_track(title=_track.title, file=_track.file, lists=request.POST.getlist("list"))
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

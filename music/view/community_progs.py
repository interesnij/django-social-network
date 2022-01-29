from music.models import *
from communities.models import Community
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import TrackForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from common.templates import render_for_platform, get_community_manage_template
from common.check.community import check_can_get_lists


class AddPlayListInCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["list_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.add_in_community_collections(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class RemovePlayListFromCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["list_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.remove_in_community_collections(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunityPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]) and list.type != MusicList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityPlaylistRecover(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityTrackRemove(View):
    def get(self, request, *args, **kwargs):
        track, c = Music.objects.get(pk=self.kwargs["track_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            track.delete_item(c)
            return HttpResponse()
        else:
            raise Http404
class CommunityTrackAbortRemove(View):
    def get(self,request,*args,**kwargs):
        track, c = Music.objects.get(pk=self.kwargs["track_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            track.restore_item(c)
            return HttpResponse()
        else:
            raise Http404

class CommunityTrackCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("music/music_create/c_create_track.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityTrackCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityTrackCreate,self).get_context_data(**kwargs)
        context["form_post"] = TrackForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = TrackForm(request.POST, request.FILES)

        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(self.kwargs["pk"]):
            track = form_post.save(commit=False)
            new_track = Music.create_track(creator=request.user, title=track.title, file=track.file, list=track.list, community=community)
            return render_for_platform(request, 'music/music_create/c_new_track.html',{'object': new_track})
        else:
            return HttpResponseBadRequest()

class CommunityTrackEdit(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["track_pk"])
        self.template_name = get_community_manage_template("music/music_create/c_edit_track.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityTrackEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityTrackEdit,self).get_context_data(**kwargs)
        context["form_post"] = TrackForm(instance=self.track)
        context["track"] = self.track
        return context

    def post(self,request,*args,**kwargs):
        self.track = Music.objects.get(pk=self.kwargs["track_pk"])
        form_post = TrackForm(request.POST, request.FILES, instance=self.track)

        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(self.kwargs["pk"]):
            _track = form_post.save(commit=False)
            new_doc = self.track.edit_track(title=_track.title, file=_track.file, list=_track.list)
            return render_for_platform(request, 'music/music_create/c_new_track.html',{'object': self.track})
        else:
            return HttpResponseBadRequest()


class CommunityChangeMusicPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.models import Community

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                post = Music.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class CommunityChangeMusicListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.model.list import CommunityDocEditPlayListPosition

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                list = CommunityPlayListPosition.objects.get(list=item['key'], community=community.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()

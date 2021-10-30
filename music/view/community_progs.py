from music.models import *
from communities.models import Community
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from music.forms import PlaylistForm, TrackForm
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from common.parsing_soundcloud.add_playlist import add_playlist
from common.templates import render_for_platform, get_community_manage_template
from common.check.community import check_can_get_lists


class CommunitySoundcloudSetPlaylistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_community_manage_template("music/music_create/c_soundcloud_add_playlist.html", request.user, Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'])
        return super(CommunitySoundcloudSetPlaylistWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunitySoundcloudSetPlaylistWindow,self).get_context_data(**kwargs)
        context['form_post'] = PlaylistForm()
        return context

class CommunitySoundcloudSetWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_community_manage_template("music/music_create/c_soundcloud_set_playlist.html", request.user, Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'])
        return super(CommunitySoundcloudSetWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunitySoundcloudSetWindow,self).get_context_data(**kwargs)
        context["list"] = self.list
        return context


class CommunitySoundcloudSetCreate(View):
    def get_context_data(self,**kwargs):
        context = super(CommunitySoundcloudSetCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post, community = PlaylistForm(request.POST), Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(community.pk):
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            new_list.community_id = community.pk
            new_list.save()
            add_playlist(request.POST.get('permalink'), request.user, new_list)
            return render_for_platform(request, 'communties/music/list/admin_list.html',{'playlist': new_list, 'object_list': new_list.get_items(),'community': community})
        else:
            return HttpResponseBadRequest()

class CommunitySoundcloudSet(View):
    def post(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            add_playlist(request.POST.get('permalink'), request.user, list)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class AddPlayListInCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.add_in_community_collections(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class RemovePlayListFromCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.remove_in_community_collections(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class AddTrackInCommunityList(View):
    def get(self, request, *args, **kwargs):
        track, list = Music.objects.get(pk=self.kwargs["pk"]), MusicList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_item_in_list(track.pk) and request.user.is_staff_of_community(list.community.pk):
            list.playlist.add(track)
            return HttpResponse()
        else:
            raise Http404

class RemoveTrackFromCommunityList(View):
    def get(self, request, *args, **kwargs):
        track, list = Music.objects.get(pk=self.kwargs["pk"]), MusicList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(track.pk) and request.user.is_staff_of_community(list.community.pk):
            list.playlist.remove(track)
            return HttpResponse()
        else:
            raise Http404

class CommunityPlaylistCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("music/music_create/c_create_list.html", request.user, self.community, request.META['HTTP_USER_AGENT'])
        return super(CommunityPlaylistCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPlaylistCreate,self).get_context_data(**kwargs)
        context["form_post"] = PlaylistForm()
        context["community"] = Community.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        form_post, community = PlaylistForm(request.POST), Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(community.pk):
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=community)
            return render_for_platform(request, 'communities/music/list/admin_list.html',{'playlist': new_list, 'community': community})
        else:
            return HttpResponseBadRequest()


class CommunityPlaylistEdit(TemplateView):
    """
    изменение плейлиста пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = get_community_manage_template("music/music_create/c_edit_list.html", request.user, self.list.community, request.META['HTTP_USER_AGENT'])
        return super(CommunityPlaylistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityPlaylistEdit,self).get_context_data(**kwargs)
        context["list"] = MusicList.objects.get(uuid=self.kwargs["uuid"])
        context["community"] = Community.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PlaylistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.is_staff_of_community(self.list.community.pk):
            list = self.form.save(commit=False)
            new_list = list.edit_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityPlaylistEdit,self).get(request,*args,**kwargs)

class CommunityPlaylistDelete(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]) and list.type != MusicList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityPlaylistRecover(View):
    def get(self,request,*args,**kwargs):
        list = MusicList.objects.get(uuid=self.kwargs["uuid"])
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
            new_track = Music.create_track(creator=request.user, title=track.title, file=track.file, list=track.list, is_public=request.POST.get("is_public"), community=community)
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
            new_doc = self.track.edit_track(title=_track.title, file=_track.file, list=_track.list, is_public=request.POST.get("is_public"))
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

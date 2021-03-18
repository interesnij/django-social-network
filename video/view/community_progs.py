from django.views.generic.base import TemplateView
from communities.models import Community
from video.models import VideoAlbum, Video, VideoComment
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from video.forms import AlbumForm, VideoForm, CommentForm
from common.check.community import check_can_get_lists
from django.views.generic import ListView
from common.template.video import get_permission_community_video
from common.template.user import render_for_platform
from common.template.community import get_community_manage_template


class CommunityVideoAlbumPreview(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.album = VideoAlbum.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_community_manage_template("communities/video/album_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityVideoAlbumPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityVideoAlbumPreview,self).get_context_data(**kwargs)
		context["album"] = self.album
		return context


class CommunityVideoAlbumAdd(View):
    def post(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.communities.add(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunityVideoAlbumRemove(View):
    def post(self,request,*args,**kwargs):
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.communities.remove(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class VideoCommentCommunityCreate(View):
	def post(self,request,*args,**kwargs):
		form_post = CommentForm(request.POST)
		community = Community.objects.get(pk=request.POST.get('pk'))
		video = Video.objects.get(uuid=request.POST.get('uuid'))
		if not community.is_comment_video_send_all() and not request.user.is_member_of_community(community.pk):
			raise PermissionDenied("Ошибка доступа.")
		elif community.is_comment_video_send_admin() and not request.user.is_staff_of_community(community.pk):
			raise PermissionDenied("Ошибка доступа.")
		elif request.is_ajax() and form_post.is_valid() and video.comments_enabled:
			comment = form_post.save(commit=False)
			check_can_get_lists(request.user, community)
			if request.POST.get('text') or request.POST.get('attach_items'):
				from common.notify.notify import community_notify

				new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, video=video, text=comment.text)
				community_notify(request.user, community, None, "com"+str(new_comment.pk)+", vid"+str(video.pk), "c_video_comment_notify", "COM")
				return render_for_platform(request, 'video/c_video_comment/admin_parent.html',{'comment': new_comment, 'community': community})
			else:
				return HttpResponseBadRequest()
		else:
			return HttpResponseBadRequest()


class VideoReplyCommunityCreate(View):
	def post(self,request,*args,**kwargs):
		form_post = CommentForm(request.POST)
		community = Community.objects.get(pk=request.POST.get('pk'))
		parent = VideoComment.objects.get(pk=request.POST.get('video_comment'))

		if not community.is_comment_video_send_all() and not request.user.is_member_of_community(community.pk):
			raise PermissionDenied("Ошибка доступа.")
		elif community.is_comment_video_send_admin() and not request.user.is_staff_of_community(community.pk):
			raise PermissionDenied("Ошибка доступа.")
		elif request.is_ajax() and form_post.is_valid() and parent.video_comment.comments_enabled:
			comment = form_post.save(commit=False)

			check_can_get_lists(request.user, community)
			if request.POST.get('text') or request.POST.get('attach_items'):
				from common.notify.notify import community_notify

				new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, video=None, text=comment.text)
				community_notify(request.user, community, None, "rep"+str(new_comment.pk)+",com"+str(parent.pk)+",pho"+str(parent.video.pk), "c_video_comment_notify", "REP")
			else:
				return HttpResponseBadRequest()
			return render_for_platform(request, 'video/c_video_comment/admin_reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
		else:
			return HttpResponseBadRequest()

class VideoCommentCommunityDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()

class VideoCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.is_deleted = True
            video.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityVideoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.is_deleted = False
            video.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.votes_on = False
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.votes_on = True
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.is_public = False
            video.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404

class CommunityOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.is_public = True
            video.save(update_fields=['is_public'])
            return HttpResponse()
        else:
            raise Http404

class CommunityVideoListCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_template_community_video(self.community, "video/community_create/", "create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityVideoListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = AlbumForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = AlbumForm(request.POST)
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community(self.community.pk):
            new_album = form_post.save(commit=False)
            new_album.creator = request.user
            new_album.community = community
            new_album.save()
            return render_for_platform(request, 'communities/video_list/admin_list.html',{'album': new_album, 'community': community})
        else:
            return HttpResponseBadRequest()


class CommunityVideoAttachCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_template_community_video(self.community, "video/community_create/", "create_video_attach.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityVideoCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoAttachCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoForm(request.POST, request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community(self.community.pk):

            my_list = VideoAlbum.objects.get(creator_id=self.user.pk, community=community, type=VideoAlbum.MAIN)
            new_video = self.form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            my_list.video_album.add(new_video)
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()


class CommunityVideoCreate(TemplateView):
    form_post = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_template_community_video(self.community, "video/community_create/", "create_video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityVideoCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoForm()
        context["album"] = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoForm(request.POST, request.FILES)
        self.community = Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community(self.community.pk):
			from common.notify.notify import community_notify

            new_video = self.form_post.save(commit=False)
            new_video.creator = request.user
            albums = request.POST.getlist("album")
            new_video.save()
            for _album_pk in albums:
                _album = VideoAlbum.objects.get(pk=_album_pk)
                _album.video_album.add(new_video)
			if new_video.is_public:
				community_notify(request.user, community, None, "vid"+str(new_video.pk), "c_video_notify", "ITE")
            return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
        else:
            return HttpResponseBadRequest()


class CommunityVideolistEdit(TemplateView):
    """
    изменение списка видео сообщества
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_manage_template("video/community_create/edit_list.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        return super(CommunityVideolistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideolistEdit,self).get_context_data(**kwargs)
        context["community"] = self.community
        context["album"] = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        self.form = AlbumForm(request.POST,instance=self.list)
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and request.user.is_staff_of_community(self.community.pk):
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityPlaylistEdit,self).get(request,*args,**kwargs)

class CommunityVideolistDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk) and list.type == VideoAlbum.ALBUM:
            list.is_deleted = True
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityVideolistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        list = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            list.is_deleted = False
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

from django.views.generic.base import TemplateView
from communities.models import Community
from video.models import VideoList, Video, VideoComment
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views import View
from video.forms import VideoListForm, VideoForm, CommentForm
from common.check.community import check_can_get_lists
from django.views.generic import ListView
from common.template.video import get_permission_community_video
from common.template.user import render_for_platform


class AddVideoListInCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.communities.add(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class RemoveVideoListFromCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
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
				community_notify(request.user, community, None, "vic"+str(new_comment.pk)+", vid"+str(video.pk), "c_video_comment_notify", "COM")
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
				community_notify(request.user, community, None, "vir"+str(new_comment.pk)+",vic"+str(parent.pk)+",pho"+str(parent.video.pk), "c_video_comment_notify", "REP")
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
            comment.delete_comment(self)
            return HttpResponse()

class VideoCommentCommunityAbortDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.abort_delete_comment(self)
            return HttpResponse()
        else:
            raise Http404

class CommunityVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video, c = Video.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community(c.pk):
            video.delete_video(c)
            return HttpResponse()
        else:
            raise Http404

class CommunityVideoAbortDelete(View):
    def get(self,request,*args,**kwargs):
        video, c = Video.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community(c.pk):
            video.abort_delete_video(c)
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
        context["form_post"] = VideoListForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoListForm(request.POST)
        self.c = Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community(self.c.pk):
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=self.c,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'communities/video_list/admin_list.html',{'list': new_list, 'community': self.c})
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

            my_list = VideoList.objects.get(creator_id=self.user.pk, community=community, type=VideoList.MAIN)
            new_video = self.form_post.save(commit=False)
            new_video.creator = request.user
            new_video.save()
            my_list.video_list.add(new_video)
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
		context["list"] = VideoList.objects.get(uuid=self.kwargs["uuid"])
		return context

	def post(self,request,*args,**kwargs):
		self.form_post = VideoForm(request.POST, request.FILES)
		self.community = Community.objects.get(pk=self.kwargs["pk"])

		if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community(self.community.pk):
			from common.notify.notify import community_notify

			new_video = self.form_post.save(commit=False)
			new_video.creator = request.user
			lists = request.POST.getlist("list")
			new_video.save()
			for _list_pk in lists:
				_list = VideoList.objects.get(pk=_list_pk)
				_list.video_list.add(new_video)
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
        context["list"] = VideoList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.form = VideoListForm(request.POST,instance=self.list)
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
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk) and list.type == VideoList.LIST:
            list.delete_list()
            return HttpResponse()
        else:
            raise Http404

class CommunityVideolistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            list.abort_delete_list()
            return HttpResponse()
        else:
            raise Http404

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
            list.add_in_community_collections(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class RemoveVideoListFromCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.remove_in_community_collections(community)
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
			if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
				new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, video=video, text=comment.text, community=community, sticker=request.POST.get('sticker'))
				return render_for_platform(request, 'video/c_video_comment/parent.html',{'comment': new_comment, 'community': community})
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
			if request.POST.get('text') or request.POST.get('attach_items') or request.POST.get('sticker'):
				new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, video=parent.video, text=comment.text, community=community, sticker=request.POST.get('sticker'))
			else:
				return HttpResponseBadRequest()
			return render_for_platform(request, 'video/c_video_comment/reply.html',{'reply': new_comment, 'comment': parent, 'community': community})
		else:
			return HttpResponseBadRequest()

class VideoCommunityCommentEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from common.templates import get_my_template
        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_my_template("video/c_post_comment/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(VideoCommunityCommentEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCommunityCommentEdit,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["form_post"] = CommentForm(instance=self.comment)
        return context

    def post(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        self.form = CommentForm(request.POST,instance=self.comment)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.comment.commenter.pk:
            from common.template.user import render_for_platform
            _comment = self.form.save(commit=False)
            new_comment = _comment.edit_comment(text=_comment.text, attach = request.POST.getlist("attach_items"))
            if self.comment.parent:
                return render_for_platform(request, 'video/c_video_comment/reply.html',{'reply': new_comment})
            else:
                return render_for_platform(request, 'video/c_video_comment/parent.html',{'comment': new_comment})
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
            comment.delete_comment()
            return HttpResponse()

class VideoCommentCommunityRecover(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        try:
            community = comment.post.community
        except:
            community = comment.parent.post.community
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            comment.restore_comment()
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

class CommunityVideoRecover(View):
    def get(self,request,*args,**kwargs):
        video, c = Video.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator_of_community(c.pk):
            video.restore_video(c)
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
            video.make_private()
            return HttpResponse()
        else:
            raise Http404

class CommunityOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_administrator_of_community(photo.community.pk):
            video.make_publish()
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
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=self.c,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'communities/video/list/admin_list.html',{'list': new_list, 'community': self.c})
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
		return context

	def post(self,request,*args,**kwargs):
		self.form_post = VideoForm(request.POST, request.FILES)
		self.community = Community.objects.get(pk=self.kwargs["pk"])

		if request.is_ajax() and self.form_post.is_valid() and request.user.is_staff_of_community(self.community.pk):
			video = self.form_post.save(commit=False)
			new_video = video.create_video(
                                            creator=request.user,
                                            title=new_video.title,
                                            file=new_video.file,
                                            uri=new_video.uri,
                                            description=new_video.description,
                                            list=new_video.list,
                                            comments_enabled=new_video.comments_enabled,
                                            votes_on=new_video.votes_on,
                                            is_public=request.POST.get("is_public"),
                                            community=self.community)
			return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
		else:
			return HttpResponseBadRequest()

class CommunityVideoEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("video/community_create/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityVideoEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideoEdit,self).get_context_data(**kwargs)
        context["form"] = VideoForm()
        context["sub_categories"] = VideoSubCategory.objects.only("id")
        context["categories"] = VideoCategory.objects.only("id")
        context["video"] = Video.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.form = VideoForm(request.POST,request.FILES, instance=self.video)
        if request.is_ajax() and self.form.is_valid() and request.user.pk.is_administrator_of_community(self.kwargs["pk"]):
            video = self.form.save(commit=False)
            new_video = self.video.edit_video(
                                        title=new_video.title,
                                        file=new_video.file,
                                        uri=new_video.uri,
                                        description=new_video.description,
                                        list=new_video.list,
                                        comments_enabled=new_video.comments_enabled,
                                        votes_on=new_video.votes_on,
                                        is_public=request.POST.get("is_public"))
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
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = self.community.get_manage_template("video/community_create/edit_list.html", request.user, self.list.community.pk, request.META['HTTP_USER_AGENT'])
        return super(CommunityVideolistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityVideolistEdit,self).get_context_data(**kwargs)
        context["list"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.form = VideoListForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.is_staff_of_community(self.list.community.pk):
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
        if request.is_ajax() and request.user.is_staff_of_community(community.pk) and list.type != VideoList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityVideolistRecover(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddVideoInCommunityList(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_item_in_list(video.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.video_list.add(video)
            return HttpResponse()
        else:
            raise Http404

class RemoveVideoFromCommunityList(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(video.pk) and request.user.is_administrator_of_community(list.community.pk):
            list.video_list.remove(video)
            return HttpResponse()
        else:
            raise Http404


class CommunityChangeVideoPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.models import Community

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                post = Video.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class CommunityChangeVideoListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from communities.model.list import CommunityVideoListPosition

        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator_of_community(community.pk):
            for item in json.loads(request.body):
                list = CommunityVideoListPosition.objects.get(list=item['key'], community=community.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()

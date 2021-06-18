
from django.views.generic.base import TemplateView
from users.models import User
from video.models import Video, VideoComment, VideoList
from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from users.models import User
from django.views.generic import ListView
from video.forms import VideoListForm, VideoForm, CommentForm
from rest_framework.exceptions import PermissionDenied
from common.template.video import get_permission_user_video
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform


class AddVideoListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemoveVideoListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class VideoCommentUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        video = Video.objects.get(uuid=request.POST.get('uuid'))

        if request.is_ajax() and form_post.is_valid() and video.comments_enabled:
            comment = form_post.save(commit=False)
            if request.user.pk != user.pk:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=None, video=video, text=comment.text, community=None)
                return render_for_platform(request, 'video/u_video_comment/parent.html',{'comment': new_comment})
            else:
                return HttpResponseBadRequest()
        else:
            return HttpResponseBadRequest()


class VideoReplyUserCreate(View):
    def post(self,request,*args,**kwargs):
        form_post = CommentForm(request.POST)
        user = User.objects.get(pk=request.POST.get('pk'))
        parent = VideoComment.objects.get(pk=request.POST.get('video_comment'))

        if request.is_ajax() and form_post.is_valid() and parent.video_comment.comments_enabled:
            comment = form_post.save(commit=False)

            if request.user != user:
                check_user_can_get_list(request.user, user)
            if request.POST.get('text') or request.POST.get('attach_items'):
                new_comment = comment.create_comment(commenter=request.user, attach=request.POST.getlist('attach_items'), parent=parent, video=parent.video, text=comment.text, community=None)
            else:
                return HttpResponseBadRequest()
            return render_for_platform(request, 'video/u_video_comment/reply.html',{'reply': new_comment, 'comment': parent, 'user': user})
        else:
            return HttpResponseBadRequest()

class VideoCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404

class VideoCommentUserRecover(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == comment.commenter.pk:
            comment.restore_item()
            return HttpResponse()
        else:
            raise Http404

class UserVideoDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserVideoRecover(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.restore_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserOpenCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = True
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserCloseCommentVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.comments_enabled = False
            video.save(update_fields=['comments_enabled'])
            return HttpResponse()
        else:
            raise Http404

class UserOffVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = False
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnVotesVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.votes_on = True
            video.save(update_fields=['votes_on'])
            return HttpResponse()
        else:
            raise Http404

class UserOnPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.make_private()
            return HttpResponse()
        else:
            raise Http404

class UserOffPrivateVideo(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and video.creator == request.user:
            video.make_publish()
            return HttpResponse()
        else:
            raise Http404

class VideoWallCommentUserDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["comment_pk"])
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == user.pk:
            comment.delete_item()
            return HttpResponse()
        else:
            raise Http404


class UserVideoCreate(TemplateView):
	form_post = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("video/user_create/", "create_video.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoCreate,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoCreate,self).get_context_data(**kwargs)
		context["form_post"] = VideoForm()
		context["list"] = VideoList.objects.get(uuid=self.kwargs["uuid"])
		return context

	def post(self,request,*args,**kwargs):
		self.form_post = VideoForm(request.POST, request.FILES)
		if request.is_ajax() and self.form_post.is_valid():
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
                                            community=None)
			return render_for_platform(request, 'video/video_new/video.html',{'object': new_video})
		else:
			return HttpResponseBadRequest()

class UserVideoEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("video/user_create/edit.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoEdit,self).get_context_data(**kwargs)
        context["form"] = VideoForm()
        context["sub_categories"] = VideoSubCategory.objects.only("id")
        context["categories"] = VideoCategory.objects.only("id")
        context["video"] = Video.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.form = VideoForm(request.POST,request.FILES, instance=self.video)
        if request.is_ajax() and self.form.is_valid() and request.user == self.user:
            video = self.form.save(commit=False)
            new_video = video.edit_video(
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


class UserVideoListCreate(TemplateView):
    form_post = None
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/create_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoListCreate,self).get_context_data(**kwargs)
        context["form_post"] = VideoListForm()
        return context

    def post(self,request,*args,**kwargs):
        self.form_post = VideoListForm(request.POST)

        if request.is_ajax() and self.form_post.is_valid():
            list = self.form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=None,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'users/video/list/my_list.html',{'list': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserVideolistEdit(TemplateView):
    """
    изменение списка видео пользователя
    """
    template_name = None
    form=None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("video/user_create/edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideolistEdit,self).get_context_data(**kwargs)
        context["list"] = VideoList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        if request.is_ajax() and self.form_post.is_valid():
            list = VideoListForm(request.POST,instance=self.list)
            new_list = list.create_list(name=list.name, description=list.description, is_public=request.POST.get("is_public"))
        return HttpResponse()

        return super(UserVideolistEdit,self).get(request,*args,**kwargs)

class UserVideolistDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == list.creator.pk and list.type != VideoList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserVideolistRecover(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.pk == list.creator.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class AddVideoInUserList(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_item_in_list(video.pk):
            list.video_list.add(video)
            return HttpResponse()
        else:
            raise Http404

class RemoveVideoFromUserList(View):
    def get(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs["pk"])
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(video.pk):
            list.video_list.remove(video)
            return HttpResponse()
        else:
            raise Http404

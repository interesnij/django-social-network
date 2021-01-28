import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from video.models import VideoAlbum, Video
from django.views.generic import ListView
from video.forms import VideoForm
from common.template.video import get_template_user_video


class UserLoadVideoAlbum(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_template_user_video(self.album, "video/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoAlbum,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserLoadVideoAlbum,self).get_context_data(**kwargs)
		c['user'], c['album'] = self.album.creator, self.album
		return c

	def get_queryset(self):
		list = self.album.get_queryset()
		return list


class UserVideoList(ListView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if self.user == request.user:
            self.video_list = self.album.get_my_queryset()
        else:
            self.video_list = self.album.get_queryset()
        self.template_name = get_template_user_video(self.album, "video/u_album_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoList,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoList,self).get_context_data(**kwargs)
        context['user'] = self.user
        context['album'] = self.album
        return context

    def get_queryset(self):
        video_list = self.video_list
        return video_list


class VideoUserCommentList(ListView):
    template_name = None
    paginate_by = 15

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.user = User.objects.get(pk=self.kwargs["pk"])
        #if not request.is_ajax() or not self.video.comments_enabled:
            #raise Http404

        self.template_name = get_permission_user_video(self.video, "video/u_video_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(VideoUserCommentList,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(VideoUserCommentList, self).get_context_data(**kwargs)
        context['parent'] = self.video
        context['user'] = self.user
        return context

    def get_queryset(self):
        comments = self.video.get_comments()
        return comments


class UserPostVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import Post
		from common.template.post import get_template_user_post

		self.post, self.user = Post.objects.get(uuid=self.kwargs["uuid"]), User.objects.get(pk=self.kwargs["pk"])
		self.video_list = self.post.get_attach_videos(), self.template_name, get_template_user_post(self.post, "video/u_album_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPostVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPostVideoList,self).get_context_data(**kwargs)
		context['user'], context['object_list'] = self.user, self.video_list
		return context


class UserPostCommentVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import PostComment
		from common.template.post import get_template_user_post

		self.comment, self.user = PostComment.objects.get(pk=self.kwargs["comment_pk"]), User.objects.get(pk=self.kwargs["pk"])
		self.video_list, self.template_name = self.comment.get_attach_videos(), get_template_user_post(self.comment.post, "video/u_album_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPostCommentVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPostCommentVideoList,self).get_context_data(**kwargs)
		context['user'], context['object_list'] = self.user, self.video_list
		return context


class UserVideoInfo(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from stst.models import VideoNumbers

		self.video, self.user = Video.objects.get(pk=self.kwargs["video_pk"]), User.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			try:
				VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
			except:
				VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, device=request.user.get_device())
		self.template_name = get_template_user_video(self.video, "video/u_video_info/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoInfo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoInfo,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['object'] = self.video
		return context


class UserVideoDetail(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from stst.models import VideoNumbers

        self.video = Video.objects.get(pk=self.kwargs["pk"])
        self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_authenticated:
            try:
                VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
            except:
                if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
                    VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=1)
                else:
                    VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=0)
        self.template_name = get_template_user_video(self.album, "video/u_video_detail/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserVideoDetail,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserVideoDetail,self).get_context_data(**kwargs)
        context['user'] = self.album.creator
        context['object'] = self.video
        return context

import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from video.models import VideoList, Video
from django.views.generic import ListView
from video.forms import VideoForm
from common.template.video import get_template_user_video


class UserLoadVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_template_user_video(self.list, "video/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserLoadVideoList,self).get_context_data(**kwargs)
		c['user'], c['list'] = self.list.creator, self.list
		return c

	def get_queryset(self):
		list = self.list.get_queryset()
		return list


class UserVideoList(ListView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.video = Video.objects.get(pk=self.kwargs["pk"])
		self.list = self.video.list
		if self.video.creator.pk == request.user.pk:
			self.video_list = self.list.get_staff_items()
		else:
			self.video_list = self.list.get_items()
		self.template_name = get_template_user_video(self.list, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.request.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.video_list


class VideoUserCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_comments

		self.video = Video.objects.get(uuid=self.kwargs["uuid"])
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if not request.is_ajax() or not self.video.comments_enabled:
			raise Http404
		self.template_name = get_template_user_comments(self.video, "video/u_video_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
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

		self.post = Post.objects.get(uuid=self.kwargs["uuid"])
		self.video_list, self.template_name = self.post.get_attach_videos(), get_template_user_post(self.post, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPostVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPostVideoList,self).get_context_data(**kwargs)
		context['object_list'] = self.video_list
		return context

class UserChatVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Chat
		from common.template.post import get_template_user_post

		self.chat = Chat.objects.get(pk=self.kwargs["pk"])
		self.video_list, self.template_name = self.chat.get_attach_videos(), get_template_user_post(self.post, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserChatVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserChatVideoList,self).get_context_data(**kwargs)
		context['object_list'] = self.video_list
		return context


class UserPostCommentVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import PostComment
		from common.template.post import get_template_user_post

		self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
		if self.comment.parent:
			post = self.comment.parent.post
		else:
			post = self.comment.post
		self.video_list, self.template_name = self.comment.get_attach_videos(), get_template_user_post(post, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPostCommentVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPostCommentVideoList,self).get_context_data(**kwargs)
		context['object_list'] = self.video_list
		return context


class UserVideoInfo(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from stst.models import VideoNumbers
		from common.templates import get_template_user_item, get_template_anon_user_item

		self.video = Video.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			try:
				VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
			except:
				VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, device=request.user.get_device())
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.video, "video/u_video_info/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.video, "video/u_video_info/anon_video.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoInfo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoInfo,self).get_context_data(**kwargs)
		context['object'] = self.video
		return context


class UserVideoDetail(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from stst.models import VideoNumbers

		self.video = Video.objects.get(pk=self.kwargs["pk"])
		self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			try:
				VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
			except:
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=1)
				else:
					VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=0)
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.video, "video/u_video_detail/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.video, "video/u_video_detail/anon_video.html", request.user, request.META['HTTP_USER_AGENT'])

	def get_context_data(self,**kwargs):
		context = super(UserVideoDetail,self).get_context_data(**kwargs)
		context['user'] = self.list.creator
		context['object'] = self.video
		return context

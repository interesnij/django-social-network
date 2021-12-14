import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from users.models import User
from video.models import VideoList, Video
from django.views.generic import ListView
from video.forms import VideoForm
from common.templates import get_template_user_item, get_template_anon_user_item


class UserVideoList(ListView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.video = Video.objects.get(pk=self.kwargs["pk"])
		self.list = self.video.list
		if self.video.creator.pk == request.user.pk:
			self.video_list = self.list.get_staff_items()
		else:
			self.video_list = self.list.get_items()

		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.video, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.video, "video/u_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.request.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.video_list


class UserPostVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import Post

		self.post = Post.objects.get(pk=self.kwargs["post_pk"])
		self.video_list = self.post.get_attach_videos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.post, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.post, "video/u_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPostVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPostVideoList,self).get_context_data(**kwargs)
		context['object_list'] = self.video_list
		return context

class UserMessageVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from chat.models import Message

		self.message = Message.objects.get(pk=self.kwargs["message_pk"])
		self.video_list = self.message.get_attach_videos()
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.video, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.video, "video/u_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserMessageVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMessageVideoList,self).get_context_data(**kwargs)
		context['object_list'] = self.video_list
		return context


class UserPostCommentVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import PostComment

		self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
		if self.comment.parent:
			post = self.comment.parent.post
		else:
			post = self.comment.post
		if request.user.is_authenticated:
			self.template_name = get_template_user_item(self.video, "video/u_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user_item(self.video, "video/u_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		self.video_list = self.comment.get_attach_videos()
		return super(UserPostCommentVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserPostCommentVideoList,self).get_context_data(**kwargs)
		context['object_list'] = self.video_list
		return context


class UserVideoInfo(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from stst.models import VideoNumbers

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
		self.list = VideoList.objects.get(pk=self.kwargs["list_pk"])
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

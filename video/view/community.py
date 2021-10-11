import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from communities.models import Community
from video.models import VideoList, Video
from django.views.generic import ListView
from video.forms import VideoForm
from common.templates import get_template_community_item, get_template_anon_community_item


class CommunityVideoList(ListView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.video = Video.objects.get(pk=self.kwargs["pk"])
		self.list = self.video.list
		self.community = self.list.community
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.post, "video/c_video_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.post, "video/c_video_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_staff_of_community(self.community.pk):
			self.video_list = self.list.get_staff_items()
		else:
			self.video_list = self.list.get_items()
		return super(CommunityVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityVideoList,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.video_list


class VideoCommunityCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_comments

		self.video = Video.objects.get(uuid=self.kwargs["uuid"])
		self.community = self.video.community
		if not request.is_ajax() or not self.video.comments_enabled:
			raise Http404
		self.template_name = get_template_user_comments(self.video, "video/c_video_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoCommunityCommentList,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(VideoCommunityCommentList, self).get_context_data(**kwargs)
		context['parent'] = self.video
		context['community'] = self.community
		return context

	def get_queryset(self):
		comments = self.video.get_comments()
		return comments


class CommunityVideoDetail(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from stst.models import VideoNumbers

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.video = Video.objects.get(uuid=self.kwargs["uuid"])
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.post, "video/c_video_detail/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.post, "video/c_video_detail/anon_video.html", request.user, request.META['HTTP_USER_AGENT'])
		if request.user.is_authenticated:
			try:
				VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
			except:
				VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, device=request.user.get_device())
		return super(CommunityVideoDetail,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityVideoDetail,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['object'] = self.video
		return context


class CommunityPostVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import Post
		from common.templates import get_template_community_item, get_template_anon_community_item

		if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.post, "video/c_video_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.post, "video/c_video_list/", "anon_list.html", request.user, request.META['HTTP_USER_AGENT'])

		self.post, self.community = Post.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityPostVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPostVideoList,self).get_context_data(**kwargs)
		context['community'], context['object_list'] = self.community, self.video_list
		return context

class CommunityPostCommentVideoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from posts.models import PostComment
		from common.templates import get_template_community_item, get_template_anon_community_item

		if request.user.is_authenticated:
            self.template_name = get_template_community_item(self.post, "video/c_video_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            self.template_name = get_template_anon_community_item(self.post, "video/c_video_list/", "anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		self.comment, self.community = PostComment.objects.get(pk=self.kwargs["comment_pk"]), Community.objects.get(pk=self.kwargs["pk"])
		return super(CommunityPostCommentVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityPostCommentVideoList,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['object_list'] = self.video_list
		return context


class CommunityVideoInfo(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from stst.models import VideoNumbers
		from common.templates import get_template_community_item, get_template_anon_community_item

		self.video = Video.objects.get(pk=self.kwargs["video_pk"])
		self.community = community.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			try:
				VideoNumbers.objects.get(user=request.user.pk, video=self.video.pk)
			except:
				if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
					VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=1)
				else:
					VideoNumbers.objects.create(user=request.user.pk, video=self.video.pk, platform=0)
		if request.user.is_authenticated:
			self.template_name = get_template_community_item(self.post, "video/c_video_info/", "video.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_community_item(self.post, "video/c_video_info/anon_video.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityVideoInfo,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommunityVideoInfo,self).get_context_data(**kwargs)
		context['community'] = self.community
		context['object'] = self.video
		return context

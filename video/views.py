from video.models import VideoList, Video
from django.views.generic import ListView
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)


class AllVideoView(ListView):
	template_name = "video.html"

	def get_queryset(self):
		return Video.objects.only("pk")


class LoadVideoList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = VideoList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_list(self.list, "video/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
			else:
				self.template_name = get_template_anon_community_list(self.list, "video/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_authenticated:
				self.template_name = get_template_user_list(self.list, "video/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.GET.get("stat"))
			else:
				self.template_name = get_template_anon_user_list(self.list, "video/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadVideoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()


class VideoCommentList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_template_user_comments, get_template_community_comments

		self.video = Video.objects.get(uuid=self.kwargs["uuid"])
		if not request.is_ajax() or not self.video.comments_enabled:
			raise Http404
		if self.video.community:
			self.template_name = get_template_user_comments(self.video, "video/c_video_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_user_comments(self.video, "video/u_video_comment/", "comments.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoCommentList,self).get(request,*args,**kwargs)

	def get_context_data(self, **kwargs):
		context = super(VideoCommentList, self).get_context_data(**kwargs)
		context['parent'] = self.video
		return context

	def get_queryset(self):
		return self.video.get_comments()

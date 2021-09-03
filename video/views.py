from video.models import VideoList, Video
from django.views.generic import ListView


class AllVideoView(ListView):
	template_name = "video.html"

	def get_queryset(self):
		return Video.objects.only("pk")


class LoadVideoList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = VideoList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			from common.templates import get_template_community_item, get_template_anon_community_item
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.list, "video/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.list, "video/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from common.templates import get_template_user_item, get_template_anon_user_item

			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.list, "video/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.list, "video/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadVideoList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()

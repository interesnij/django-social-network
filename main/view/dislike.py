from django.views.generic import ListView
from django.http import Http404
from common.user_progs.timelines_dislikes import *
from common.template.user import get_settings_template, get_detect_main_template


class PostDislikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostDislikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_post_dislikes_for_user(self.request.user).order_by('-created')
		else:
			items = []
		return items


class PhotoDislikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoDislikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photo_dislikes_for_user(self.request.user)
		else:
			items = []
		return items


class GoodDislikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodDislikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_good_dislikes_for_user(self.request.user)
		else:
			items = []
		return items


class VideoDislikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoDislikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_video_dislikes_for_user(self.request.user)
		else:
			items = []
		return items

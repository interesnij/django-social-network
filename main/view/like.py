from django.views.generic import ListView
from common.user_progs.timelines_likes import *
from common.template.user import get_settings_template, get_detect_main_template


class PostLikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostLikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_post_likes_for_user(self.request.user).order_by('-created')
		else:
			items = []
		return items


class PhotoLikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoLikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photo_likes_for_user(self.request.user)
		else:
			items = []
		return items


class GoodLikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodLikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_good_likes_for_user(self.request.user)
		else:
			items = []
		return items


class VideoLikesListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoLikesListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_video_likes_for_user(self.request.user)
		else:
			items = []
		return items

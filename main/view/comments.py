from django.views.generic import ListView
from common.user_progs.timelines_comments import *
from common.template.user import get_settings_template, get_detect_main_template


class PostCommentsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostCommentsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_post_comments_for_user(self.request.user).order_by('-created')
		else:
			items = []
		return items


class PhotoCommentsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoCommentsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photo_comments_for_user(self.request.user)
		else:
			items = []
		return items


class GoodCommentsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodCommentsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_good_comments_for_user(self.request.user)
		else:
			items = []
		return items


class VideoCommentsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoCommentsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_video_comments_for_user(self.request.user)
		else:
			items = []
		return items

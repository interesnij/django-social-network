from django.views.generic import ListView
from django.http import Http404
from common.user_progs.timelines import *
from common.template.user import get_settings_template, get_detect_main_template


class PostsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_posts_for_user(self.request.user).order_by('-created')
		else:
			items = []
		return items


class PhotosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotosListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photos_for_user(self.request.user)
		else:
			items = []
		return items


class GoodsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_goods_for_user(self.request.user)
		else:
			items = []
		return items


class VideosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideosListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_videos_for_user(self.request.user)
		else:
			items = []
		return items


class AudiosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/audios.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AudiosListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_audios_for_user(self.request.user)
		else:
			items = []
		return items

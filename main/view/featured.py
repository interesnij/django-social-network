from django.views.generic import ListView
from django.http import Http404
from common.user_progs.timelines import *
from common.template.user import get_settings_template, get_detect_main_template


class FeaturedPostsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPostsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_posts_for_possible_users(self.request.user)
		else:
			items = []
		return items


class FeaturedPhotosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPhotosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photos_for_possible_users(self.request.user)
		else:
			items = []
		return items


class FeaturedGoodsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedGoodsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_goods_for_possible_users(self.request.user)
		else:
			items = []
		return items


class FeaturedVideosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedVideosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_videos_for_possible_users(self.request.user)
		else:
			items = []
		return items

class FeaturedAudiosView(ListView):
	template_name = None
	paginate_by = 15
	items = []

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/audios.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedAudiosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.items

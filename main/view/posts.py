from django.views.generic import ListView
from common.user_progs.timelines_post import *
from common.template.user import get_settings_template, get_detect_main_template


class PhotosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photos(self.request.user)
		else:
			items = []
		return items


class GoodsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_goods(self.request.user)
		else:
			items = []
		return items


class VideosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_videos(self.request.user)
		else:
			items = []
		return items


class AudiosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/news/audios.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AudiosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_audios(self.request.user)
		else:
			items = []
		return items


class FeaturedPostsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPostsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_posts(self.request.user)
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
			items = get_timeline_featured_photos(self.request.user)
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
			items = get_timeline_featured_goods(self.request.user)
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
			items = get_timeline_featured_videos(self.request.user)
		else:
			items = []
		return items


class FeaturedAudiosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/audios.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedAudiosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_audios(self.request.user)
		else:
			items = []
		return items

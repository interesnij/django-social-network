from django.views.generic import ListView
from common.user_progs.timelines_likes import *
from common.template.user import get_settings_template, get_detect_main_template


class PostLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_post_likes(self.request.user).order_by('-created')
		else:
			items = []
		return items


class PhotoLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photo_likes(self.request.user)
		else:
			items = []
		return items


class GoodLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_good_likes(self.request.user)
		else:
			items = []
		return items


class VideoLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_video_likes(self.request.user)
		else:
			items = []
		return items


class FeaturedPostLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/featured_posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPostLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_post_likes(self.request.user).order_by('-created')
		else:
			items = []
		return items


class FeaturedPhotoLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/featured_photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPhotoLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_photo_likes(self.request.user)
		else:
			items = []
		return items


class FeaturedGoodLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/featured_goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedGoodLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_good_likes(self.request.user)
		else:
			items = []
		return items


class FeaturedVideoLikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/likes/featured_videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedVideoLikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_video_likes(self.request.user)
		else:
			items = []
		return items

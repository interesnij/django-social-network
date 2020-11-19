from django.views.generic import ListView
from common.user_progs.timelines_dislikes import *
from common.template.user import get_settings_template, get_detect_main_template


class PostDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_post_dislikes(self.request.user).order_by('-created')
		else:
			items = []
		return items


class PhotoDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photo_dislikes(self.request.user)
		else:
			items = []
		return items


class GoodDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_good_dislikes(self.request.user)
		else:
			items = []
		return items


class VideoDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_video_dislikes(self.request.user)
		else:
			items = []
		return items


class FeaturedPostDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/featured_posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPostDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_post_dislikes(self.request.user).order_by('-created')
		else:
			items = []
		return items


class FeaturedPhotoDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/featured_photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPhotoDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_photo_dislikes(self.request.user)
		else:
			items = []
		return items


class FeaturedGoodDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/featured_goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedGoodDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_good_dislikes(self.request.user)
		else:
			items = []
		return items


class FeaturedVideoDislikesView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/dislikes/featured_videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedVideoDislikesView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_video_dislikes(self.request.user)
		else:
			items = []
		return items

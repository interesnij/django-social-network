from django.views.generic import ListView
from common.user_progs.timelines_comments import *
from common.template.user import get_settings_template, get_detect_main_template


class PostCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PostCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_post_comments(self.request.user.pk).order_by('-created')
		else:
			items = []
		return items


class PhotoCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(PhotoCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photo_comments(self.request.user.pk)
		else:
			items = []
		return items


class GoodCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(GoodCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_good_comments(self.request.user.pk)
		else:
			items = []
		return items


class VideoCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(VideoCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_video_comments(self.request.user.pk)
		else:
			items = []
		return items


class FeaturedPostCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/featured_posts.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPostCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_post_comments(self.request.user).order_by('-created')
		else:
			items = []
		return items


class FeaturedPhotoCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/featured_photos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedPhotoCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_photo_comments(self.request.user)
		else:
			items = []
		return items


class FeaturedGoodCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/featured_goods.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedGoodCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_good_comments(self.request.user)
		else:
			items = []
		return items


class FeaturedVideoCommentsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/comments/featured_videos.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedVideoCommentsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_featured_video_comments(self.request.user)
		else:
			items = []
		return items

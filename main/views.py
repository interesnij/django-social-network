import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import Http404
from common.user_progs.timelines import *
from common.template.user import get_settings_template


class PostsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/news/posts.html", request)
		else:
			self.template_name = "main/auth.html"
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return super(PostsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_posts_for_user(self.request.user).order_by('-created')
		else:
			items = []
		return items

class FeaturedPostsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/featured/posts.html", request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedPostsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_posts_for_possible_users(self.request.user)
		else:
			items = []
		return items


class PhotosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/news/photos.html", request)
		else:
			self.template_name = "main/auth.html"
		return super(PhotosListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photos_for_user(self.request.user)
		else:
			items = []
		return items

class FeaturedPhotosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/featured/photos.html", request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedPhotosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photos_for_possible_users(self.request.user)
		else:
			items = []
		return items


class GoodsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/news/goods.html", request)
		else:
			self.template_name = "main/auth.html"
		return super(GoodsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_goods_for_user(self.request.user)
		else:
			items = []
		return items

class FeaturedGoodsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/featured/goods.html", request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedGoodsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_goods_for_possible_users(self.request.user)
		else:
			items = []
		return items


class VideosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/news/videos.html", request)
		else:
			self.template_name = "main/auth.html"
		return super(VideosListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_videos_for_user(self.request.user)
		else:
			items = []
		return items

class FeaturedVideosView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/featured/videos.html", request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedVideosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_videos_for_possible_users(self.request.user)
		else:
			items = []
		return items

class AudiosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/news/audios.html", request)
		else:
			self.template_name = "main/auth.html"
		return super(AudiosListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_audios_for_user(self.request.user)
		else:
			items = []
		return items

class FeaturedAudiosView(ListView):
	template_name = None
	paginate_by = 15
	items = []

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = get_settings_template("news_list/featured/audios.html", request)
			self.items = get_timeline_audios_for_possible_users(request.user)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedAudiosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.items


class MainPhoneSend(TemplateView):
	template_name = "phone_verification.html"

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("main/phone_verification.html", request)
		return super(MainPhoneSend,self).get(request,*args,**kwargs)

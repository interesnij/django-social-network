from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import Http404
from common.user_progs.timelines import *

class PostsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="news_list/", template="posts.html", request=request)
		else:
			self.template_name = "main/auth.html"
		return super(PostsListView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_posts_for_user(self.request.user)
		else:
			items = []
		return items

class FeaturedPostsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="news_list/", template="featured_posts.html", request=request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedPostsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_posts_for_possible_users(self.request.user)
		else:
			items = None
		return items


class PhotosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="news_list/", template="photos.html", request=request)
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
			self.template_name = request.user.get_settings_template(folder="news_list/", template="featured_photos.html", request=request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedPhotosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_photos_for_possible_users(self.request.user)
		else:
			items = None
		return items


class GoodsListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="news_list/", template="goods.html", request=request)
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
			self.template_name = request.user.get_settings_template(folder="news_list/", template="featured_goods.html", request=request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedGoodsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_goods_for_possible_users(self.request.user)
		else:
			items = None
		return items


class VideosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="news_list/", template="videos.html", request=request)
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
			self.template_name = request.user.get_settings_template(folder="news_list/", template="featured_videos.html", request=request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedVideosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_videos_for_possible_users(self.request.user)
		else:
			items = None
		return items

class AudiosListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="news_list/", template="audios.html", request=request)
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

	def get(self,request,*args,**kwargs):
		if request.user.is_authenticated:
			self.template_name = request.user.get_settings_template(folder="news_list/", template="featured_audios.html", request=request)
		else:
			self.template_name = 'main/auth.html'
		return super(FeaturedAudiosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		if self.request.user.is_authenticated:
			items = get_timeline_audios_for_possible_users(self.request.user)
		else:
			items = None
		return items


class ComingView(TemplateView):
	template_name = "base_coming.html"


class MainPhoneSend(TemplateView):
	template_name = "phone_verification.html"

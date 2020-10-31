import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.http import Http404
from common.user_progs.timelines import *
from common.template.user import get_settings_template


def get_detect_main_template(template, request_user, user_agent):
	""" получаем название шаблона для новостей и рекомендаций. Направляем или в новости, или на страницу входа, исходя из платформы пользователя """
	if MOBILE_AGENT_RE.match(user_agent):
		if request_user.is_authenticated:
			template_name = "mobile/" + template
		else:
			template_name = "mobile/main/auth.html"
	else:
		if request_user.is_authenticated:
			template_name = "desctop/" + template
		else:
			template_name = "desctop/main/auth.html"
	return template_name

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

class FeaturedAudiosView(ListView):
	template_name = None
	paginate_by = 15
	items = []

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/news_list/featured/audios.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FeaturedAudiosView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.items


class MainPhoneSend(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		self.template_name = get_detect_main_template("main/phone_verification.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(MainPhoneSend,self).get(request,*args,**kwargs)

from users.models import User
from django.views.generic import ListView
from posts.models import Post, PostsList
from django.http import Http404
from django.db.models import Q
from common.templates import get_template_anon_user_list, get_template_user_list, get_settings_template, get_detect_platform_template
from django.views.generic.base import TemplateView


class UserVisitCommunities(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/user_community/visited_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVisitCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.request.user.get_visited_communities()

class BlackListUsers(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/u_list/blacklist.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(BlackListUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.request.user.get_blocked_users()


class UserVideoList(ListView):
	template_name, paginate_by, is_user_can_see_video_section, is_user_can_see_video_list, is_user_can_create_videos = None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		from video.models import VideoList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			if request.user.pk == self.list.creator.pk:
				self.is_user_can_see_video_section = True
				self.is_user_can_see_video_list = True
				self.is_user_can_create_videos = True
			else:
				self.is_user_can_see_video_section = True
				self.is_user_can_see_video_list = self.list.is_user_can_see_el(request.user.pk)
				self.is_user_can_create_videos = self.list.is_user_can_create_el(request.user.pk)
		else:
			self.is_user_can_see_video_section = self.user.is_user_can_see_video(request.user.pk)
			self.is_user_can_see_video_list = self.list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_videos = self.list.is_user_can_create_el(request.user.pk)
		if request.user.is_anonymous:
			self.template_name = get_template_anon_user_list(self.list, "users/video/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			self.is_user_can_see_video_section = self.user.is_anon_user_can_see_video()
			self.is_user_can_see_video_list = self.list.is_anon_user_can_see_el()
		else:
			self.template_name = get_template_user_list(self.list, "users/video/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['is_user_can_see_video_section'] = self.is_user_can_see_video_section
		context['is_user_can_see_video_list'] = self.is_user_can_see_video_list
		context['is_user_can_create_videos'] = self.is_user_can_create_videos
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserPhotoList(TemplateView):
	template_name, is_user_can_see_photo_section, is_user_can_see_photo_list, is_user_can_create_photos = None, None, None, None

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			if request.user.pk == self.list.creator.pk:
				self.is_user_can_see_photo_section = True
				self.is_user_can_see_photo_list = True
				self.is_user_can_create_photos = True
			else:
				self.is_user_can_see_photo_section = True
				self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
				self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)
		else:
			self.is_user_can_see_photo_section = self.user.is_user_can_see_photo(request.user.pk)
			self.is_user_can_see_photo_list = self.list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_photos = self.list.is_user_can_create_el(request.user.pk)

		if request.user.is_anonymous:
			self.template_name = get_template_anon_user_list(self.list, "users/photos/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			self.is_user_can_see_photo_section = self.user.is_anon_user_can_see_photo()
			self.is_user_can_see_photo_list = self.list.is_anon_user_can_see_el()
		else:
			self.template_name = get_template_user_list(self.list, "users/photos/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserPhotoList,self).get_context_data(**kwargs)
		c['user'], c['list'], c['is_user_can_see_photo_section'], \
		c['is_user_can_see_photo_list'], c['is_user_can_create_photos'] = self.user, \
		self.list, self.is_user_can_see_photo_section, self.is_user_can_see_photo_list, self.is_user_can_create_photos
		return c


class UserGoodsList(ListView):
	template_name, paginate_by, is_user_can_see_good_section, is_user_can_see_good_list, is_user_can_create_goods = None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		from goods.models import GoodList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = GoodList.objects.get(uuid=self.kwargs["uuid"])

		if self.user.pk == request.user.pk:
			if request.user.pk == self.list.creator.pk:
				self.is_user_can_see_good_section = True
				self.is_user_can_see_good_list = True
				self.is_user_can_create_goods = True
			else:
				self.is_user_can_see_good_section = True
				self.is_user_can_see_good_list = self.list.is_user_can_see_el(request.user.pk)
				self.is_user_can_create_goods = self.list.is_user_can_create_el(request.user.pk)
		else:
			self.is_user_can_see_good_section = self.user.is_user_can_see_good(request.user.pk)
			self.is_user_can_see_good_list = self.list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_goods = self.list.is_user_can_create_el(request.user.pk)
		if request.user.is_anonymous:
			self.template_name = get_template_anon_user_list(self.list, "users/goods/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			self.is_user_can_see_good_section = self.user.is_anon_user_can_see_good()
			self.is_user_can_see_good_list = self.list.is_anon_user_can_see_el()
		else:
			self.template_name = get_template_user_list(self.list, "users/goods/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserGoodsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserGoodsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['is_user_can_see_good_section'] = self.is_user_can_see_good_section
		context['is_user_can_see_good_list'] = self.is_user_can_see_good_list
		context['is_user_can_create_goods'] = self.is_user_can_create_goods
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserMusicList(ListView):
	template_name, paginate_by, is_user_can_see_music_section, is_user_can_see_music_list, is_user_can_create_tracks = None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		from music.models import MusicList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			if request.user.pk == self.list.creator.pk:
				self.is_user_can_see_music_section = True
				self.is_user_can_see_music_list = True
				self.is_user_can_create_tracks = True
			else:
				self.is_user_can_see_music_section = True
				self.is_user_can_see_music_list = self.list.is_user_can_see_el(request.user.pk)
				self.is_user_can_create_tracks = self.list.is_user_can_create_el(request.user.pk)
		else:
			self.is_user_can_see_music_section = self.user.is_user_can_see_music(request.user.pk)
			self.is_user_can_see_music_list = self.list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_tracks = self.list.is_user_can_create_el(request.user.pk)
		if request.user.is_anonymous:
			self.template_name = get_template_anon_user_list(self.list, "users/music/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			self.is_user_can_see_music_section = self.user.is_anon_user_can_see_music()
			self.is_user_can_see_music_list = self.list.is_anon_user_can_see_el()
		else:
			self.template_name = get_template_user_list(self.list, "users/music/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusicList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['is_user_can_see_music_section'] = self.is_user_can_see_music_section
		context['is_user_can_see_music_list'] = self.is_user_can_see_music_list
		context['is_user_can_create_tracks'] = self.is_user_can_create_tracks
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserDocsList(ListView):
	template_name, paginate_by, is_user_can_see_doc_section, is_user_can_see_doc_list, is_user_can_create_docs = None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		from docs.models import DocsList

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), DocsList.objects.get(uuid=self.kwargs["uuid"])

		if self.user.pk == request.user.pk:
			if request.user.pk == self.list.creator.pk:
				self.is_user_can_see_doc_section = True
				self.is_user_can_see_doc_list = True
				self.is_user_can_create_docs = True
			else:
				self.is_user_can_see_doc_section = True
				self.is_user_can_see_doc_list = self.list.is_user_can_see_el(request.user.pk)
				self.is_user_can_create_docs = self.list.is_user_can_create_el(request.user.pk)
		else:
			self.is_user_can_see_doc_section = self.user.is_user_can_see_doc(request.user.pk)
			self.is_user_can_see_doc_list = self.list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_docs = self.list.is_user_can_create_el(request.user.pk)
		if request.user.is_anonymous:
			self.template_name = get_template_anon_user_list(self.list, "users/docs/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			self.is_user_can_see_doc_section = self.user.is_anon_user_can_see_doc()
			self.is_user_can_see_doc_list = self.list.is_anon_user_can_see_el()
		else:
			self.template_name = get_template_user_list(self.list, "users/docs/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		context['is_user_can_see_doc_section'] = self.is_user_can_see_doc_section
		context['is_user_can_see_doc_list'] = self.is_user_can_see_doc_list
		context['is_user_can_create_docs'] = self.is_user_can_create_docs
		return context

	def get_queryset(self):
		return self.list.get_items()


class AllFeaturedUsersList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/u_list/featured_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllFeaturedUsersList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(AllFeaturedUsersList,self).get_context_data(**kwargs)
		context['user'] = self.request.user
		return context

	def get_queryset(self):
		return self.request.user.get_featured_friends()

class AllFeaturedCommunitiesList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/u_list/featured_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllFeaturedCommunitiesList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(AllFeaturedCommunitiesList,self).get_context_data(**kwargs)
		context['user'] = self.request.user
		return context

	def get_queryset(self):
		return self.request.user.get_featured_communities()


class AllUsers(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.templates import get_default_template

		self.template_name = get_default_template("users/u_list/", "all_users.html", request.user, request.META['HTTP_USER_AGENT'])
		all_query = ~Q(type__contains="_")
		if request.user.is_anonymous or request.user.is_child():
			all_query.add(~Q(Q(type=User.VERIFIED_SEND)|Q(type=User.STANDART)), Q.AND)
		self.all_users = User.objects.filter(all_query)
		return super(AllUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.all_users

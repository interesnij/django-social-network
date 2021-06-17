from users.models import User
from django.views.generic import ListView
from posts.models import Post, PostList
from common.template.user import get_settings_template, get_detect_platform_template
from django.http import Http404
from django.db.models import Q
from common.templates import get_template_anon_user, get_template_user
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
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoList
		from common.template.video import get_template_user_video

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.video_list = self.list.get_staff_items()
		else:
			self.video_list = self.list.get_items()
		if self.list.type == VideoList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/video/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/video/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/video/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/video/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_video_manager())
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.video_list


class UserPhotoList(TemplateView):
	template_name = None

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
		if self.list.type == PhotoList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/photos/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/photos/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/photos/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/photos/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_photo_manager())
		return super(UserPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserPhotoList,self).get_context_data(**kwargs)
		c['user'], c['list'] = self.user, self.list
		return c


class UserGoodsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodList
		from common.template.good import get_template_user_good

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = GoodList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			self.goods_list = self.list.get_staff_items()
		else:
			self.goods_list = self.list.get_items()
		if self.list.type == GoodList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/goods/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/goods/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_good_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/goods/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/goods/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_good_manager())
		return super(UserGoodsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserGoodsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.goods_list


class UserMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = SoundList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			self.sound_list = self.list.get_staff_items()
		else:
			self.sound_list = self.list.get_items()
		if self.list.type == SoundList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/music/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/music/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/music/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/music/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
		return super(UserMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusicList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.list.get_items()


class UserDocsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		from common.template.doc import get_template_user_doc

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			self.doc_list = self.list.get_staff_items()
		else:
			self.doc_list = self.list.get_items()
		if self.list.type == DocList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/docs/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/docs/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user(self.list, "users/docs/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user(self.list, "users/docs/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_audio_manager())
		return super(UserDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.doc_list


class AllPossibleUsersList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/u_list/possible_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllPossibleUsersList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(AllPossibleUsersList,self).get_context_data(**kwargs)
		context['user'] = self.request.user
		return context

	def get_queryset(self):
		return self.request.user.get_possible_friends()

class UserPostsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from posts.models import PostList
		from common.templates import get_template_user, get_template_anon_user

		self.user, user_pk, self.post_list = User.objects.get(pk=self.kwargs["pk"]), int(self.kwargs["pk"]), PostList.objects.get(pk=self.kwargs["list_pk"])
		if user_pk == request.user.pk:
			self.list = self.post_list.get_staff_items()
			self.post_lists = PostList.get_user_staff_lists(user_pk)
		else:
			self.list = self.post_list.get_items()
			self.post_lists = PostList.get_user_lists(user_pk)
		if request.user.is_authenticated:
			self.template_name = get_template_user(self.post_list, "users/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'], request.user.is_post_manager())
		else:
			self.template_name = get_template_anon_user(self.post_list, "users/lenta/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPostsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserPostsListView,self).get_context_data(**kwargs)
		c['user'], c['post_lists'], c['fix_list'], c['list'] = self.user, self.post_lists, self.user.get_fix_list(), self.post_list
		return c

	def get_queryset(self):
		return self.list


class AllUsers(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.user import get_default_template

		self.template_name = get_default_template("users/u_list/", "all_users.html", request.user, request.META['HTTP_USER_AGENT'])
		all_query = ~Q(type__contains="_")
		if request.user.is_anonymous or request.user.is_child():
			all_query.add(~Q(Q(type=User.VERIFIED_SEND)|Q(type=User.STANDART)), Q.AND)
		self.all_users = User.objects.filter(all_query)
		return super(AllUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.all_users

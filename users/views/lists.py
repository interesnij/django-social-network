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
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.video_list = self.list.get_staff_items()
		else:
			self.video_list = self.list.get_items()
		if self.list.type == VideoList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/video/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/video/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/video/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/video/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.video_list


class UserPhotoList(TemplateView):
	template_name, is_user_can_see_photo_section = None, None

	def get(self,request,*args,**kwargs):
		from gallery.models import PhotoList

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), PhotoList.objects.get(uuid=self.kwargs["uuid"])
		if request.user.pk == self.list.creator.pk:
			self.is_user_can_see_photo_section = True
		elif request.user.pk == self.user.pk:
			self.is_user_can_see_photo_section = True
			
		if self.list.type == PhotoList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/photos/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/photos/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/photos/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/photos/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPhotoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserPhotoList,self).get_context_data(**kwargs)
		c['user'], c['list'] = self.user, self.list
		return c


class UserGoodsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = GoodList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			self.goods_list = self.list.get_staff_items()
		else:
			self.goods_list = self.list.get_items()
		if self.list.type == GoodList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/goods/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/goods/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/goods/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/goods/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
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
		from music.models import MusicList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = MusicList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			self.sound_list = self.list.get_staff_items()
		else:
			self.sound_list = self.list.get_items()
		if self.list.type == MusicList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/music/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/music/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/music/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/music/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
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
		from docs.models import DocsList

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), DocsList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			self.doc_list = self.list.get_staff_items()
		else:
			self.doc_list = self.list.get_items()
		if self.list.type == DocsList.MAIN:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/docs/main_list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/docs/main_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "users/docs/list/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_user_list(self.list, "users/docs/list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		return self.doc_list


class AllFeaturedUsersList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/u_list/featured_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllFeaturedUsersList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(AllFeaturedUsersList,self).get_context_data(**kwargs)
		context['user'] = self.request.user
		return context

	def get_queryset(self):
		return self.request.user.get_featured_friends()

class UserPostsListView(ListView):
	template_name, paginate_by, is_user_can_see_post_section, is_user_can_see_post_list, is_user_can_create_posts = None, 15, None, None, None

	def get(self,request,*args,**kwargs):
		""" is_user_can_see_post_section - может ли гость видеть раздел записей
			is_user_can_create_posts - может ли гость создавать записи в списках того, к кому зашел
		"""
		from posts.models import PostsList
		from common.templates import get_owner_template_user, get_template_anon_user_list

		self.user, user_pk, self.post_list = User.objects.get(pk=self.kwargs["pk"]), int(self.kwargs["pk"]), PostsList.objects.get(pk=self.kwargs["list_pk"])
		if user_pk == request.user.pk:
			self.post_lists = PostsList.get_user_staff_lists(user_pk)
			if (self.post_list.community and request.user.is_administrator_of_community(self.post_list.community.pk)) \
			or (not self.post_list.community and request.user.pk == self.post_list.creator.pk):
				""" Это страница пользователя. Мы проверяем полномочия его в отношении списка по
					умолчанию первого. Если список имеет сообщество и пользователь его админ или
					не имеет сообщество и он его создатель, тогда особые права.
					Потому он может:
					- видеть записи пользователя is_user_can_see_post_section,
					- видеть этот список is_user_can_see_post_list,
					- создавать записи в этом список is_user_can_create_posts
				"""
				self.list = self.post_list.get_staff_items()
				self.is_user_can_see_post_section = True
				self.is_user_can_see_post_list = True
				self.is_user_can_create_posts = True
			else:
				""" создатель активного списка на своей странице и это его пост.
					Потому проверяем, может ли:
					видеть записи пользователя is_user_can_see_post_section - да,
					видеть этот список is_user_can_see_post_list,
					создавать записи в этом список is_user_can_create_posts
				"""
				self.list = self.post_list.get_items()
				self.is_user_can_see_post_section = True
				self.is_user_can_see_post_list = self.post_list.is_user_can_see_el(request.user.pk)
				self.is_user_can_create_posts = self.post_list.is_user_can_create_el(request.user.pk)
		else:
			""" Гость - пользователь
				Потому проверяем, может ли:
				видеть записи пользователя is_user_can_see_post_section - да,
				видеть этот список is_user_can_see_post_list,
				создавать записи в этом список is_user_can_create_posts
			"""
			self.is_user_can_see_post_section = self.user.is_user_can_see_post(request.user.pk)
			self.is_user_can_see_post_list = self.post_list.is_user_can_see_el(request.user.pk)
			self.is_user_can_create_posts = self.post_list.is_user_can_create_el(request.user.pk)

			self.list = self.post_list.get_items()
			self.post_lists = PostsList.get_user_lists(user_pk)

		if request.user.is_authenticated:
			self.template_name =  get_template_user_list(self.post_list, "users/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			""" Анонимный пользователь
				Потому проверяем, может ли:
				видеть записи пользователя is_user_can_see_post_section - да,
				видеть этот список is_user_can_see_post_list
			"""
			self.template_name = get_template_anon_user_list(self.post_list, "users/lenta/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
			self.is_user_can_see_post_section = self.user.is_anon_user_can_see_post()
			self.is_user_can_see_post_list = self.post_list.is_anon_user_can_see_el()
			self.post_lists = PostsList.get_user_lists(user_pk)
		return super(UserPostsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserPostsListView,self).get_context_data(**kwargs)
		c['user'],c['post_lists'],c['fix_list'],c['list'],c['is_user_can_see_post_section'],c['is_user_can_see_post_list'],c['is_user_can_create_posts'] = self.user,self.post_lists,self.user.get_fix_list(),self.post_list,self.is_user_can_see_post_section,self.is_user_can_see_post_list, self.is_user_can_create_posts
		return c

	def get_queryset(self):
		return self.list


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

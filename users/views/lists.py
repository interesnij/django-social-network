from users.models import User
from django.views.generic import ListView
from posts.models import Post, PostList
from common.template.user import get_settings_template
from django.http import Http404


class UserVisitCommunities(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/user_community/visited_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVisitCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		communities = self.request.user.get_visited_communities()
		return communities

class BlackListUsers(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/u_list/blacklist.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(BlackListUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		communities = self.request.user.get_blocked_users()
		return communities


class UserVideoList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum
		from common.template.video import get_template_user_video

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.video_list = self.album.get_my_queryset()
		else:
			self.video_list = self.album.get_queryset()
		if self.album.type == VideoAlbum.MAIN:
			self.template_name = get_template_user_video(self.user, "users/user_video/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_user_video(self.user, "users/user_video_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['album'] = self.album
		return context

	def get_queryset(self):
		video_list = self.video_list
		return video_list


class UserGoodsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum
		from common.template.good import get_template_user_good

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.album = GoodAlbum.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.goods_list = self.album.get_staff_goods()
		else:
			self.goods_list = self.album.get_goods()
		if self.album.type == GoodAlbum.MAIN:
			self.template_name = get_template_user_good(self.user, "users/user_goods/", "goods.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_user_good(self.user, "users/user_goods_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserGoodsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserGoodsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['album'] = self.album
		return context

	def get_queryset(self):
		goods_list = self.goods_list
		return goods_list


class UserMusicList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList
		from common.template.music import get_template_user_music

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
		if self.playlist.type == SoundList.MAIN:
			self.template_name = get_template_user_music(self.user, "users/user_music/", "music.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_user_music(self.user, "users/user_music_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusicList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['playlist'] = self.playlist
		return context

	def get_queryset(self):
		playlist = self.playlist.playlist_too()
		return playlist


class UserDocsList(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList
		from common.template.doc import get_template_user_doc

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
		if self.user.pk == request.user.pk:
			self.doc_list = self.list.get_my_docs()
		else:
			self.doc_list = self.list.get_docs()
		if self.list.type == DocList.MAIN:
			self.template_name = get_template_user_doc(self.user, "users/user_docs/", "docs.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_user_doc(self.user, "users/user_docs_list/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDocsList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDocsList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		doc_list = self.doc_list
		return doc_list


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
		possible_list = self.user.get_possible_friends()
		return possible_list

class UserPostsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.post import get_permission_user_post

		self.user, self.list = User.objects.get(pk=self.kwargs["pk"]), PostList.objects.get(pk=self.kwargs["list_pk"])
		if (self.user.pk != request.user.pk and self.list.is_private_list()) or not request.is_ajax():
			raise Http404
		else:
			self.posts_list = self.list.get_posts()
		self.template_name = get_permission_user_post(self.user, "users/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserPostsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(UserPostsListView,self).get_context_data(**kwargs)
		c['user'], c['list'] = self.user, self.list
		return c

	def get_queryset(self):
		return self.posts_list


class AllUsers(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		from common.template.user import get_default_template

		self.template_name = get_default_template("users/u_list/", "all_users.html", request.user, request.META['HTTP_USER_AGENT'])
		all_query = Q()
		all_query.add(~Q(Q(perm=User.DELETED)|Q(perm=User.BLOCKED)|Q(perm=User.PHONE_NO_VERIFIED)), Q.AND)
		if request.user.is_anonymous or request.user.is_child():
			all_query.add(~Q(Q(perm=User.VERIFIED_SEND)|Q(perm=User.STANDART)), Q.AND)
		self.all_users = User.objects.filter(all_query)
		return super(AllUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.all_users


from users.models import User
from django.views.generic import ListView
from posts.models import Post
from common.template.post import get_permission_user_post
from common.template.video import get_template_user_video
from common.template.music import get_template_user_music
from common.template.user import get_settings_template
from common.template.good import get_template_user_good
from common.template.doc import get_template_user_doc
from common.template.user import get_default_template
from django.http import Http404



class UserVisitCommunities(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("users/user_community/visited_communities.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserVisitCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		communities = self.request.user.get_visited_communities()
		return communities

class BlackListUsers(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("users/u_list/blacklist.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(BlackListUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		communities = self.request.user.get_blocked_users()
		return communities


class UserVideoList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

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
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from goods.models import GoodAlbum

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
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList

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
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from docs.models import DocList

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
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
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = get_settings_template("users/u_list/possible_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllPossibleUsersList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(AllPossibleUsersList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		possible_list = self.user.get_possible_friends()
		return possible_list

class PostListView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax():
			self.template_name = get_permission_user_post(self.user, "users/lenta/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			raise Http404
		return super(PostListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PostListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['object'] = self.user.get_fixed_post()
		return context

	def get_queryset(self):
		posts_list = self.user.get_posts().order_by('-created')
		return posts_list


class AllUsers(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_default_template("users/u_list/", "all_users.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(AllUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.request.user.get_all_users()

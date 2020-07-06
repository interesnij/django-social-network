import re
from users.models import User
from django.views.generic import ListView
from django.shortcuts import render_to_response
from posts.models import Post
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from rest_framework.exceptions import PermissionDenied


class UserVisitCommunities(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = request.user.get_settings_template(folder="user_community/", template="visits.html", request=request)
		return super(UserVisitCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		communities = self.request.user.get_visited_communities()
		return communities


class UserVideoList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from video.models import VideoAlbum

		self.template_name = request.user.get_template_user(folder="user_video_list/", template="list.html", request=request)
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.album = VideoAlbum.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.video_list = self.album.get_my_queryset()
		else:
			self.video_list = self.album.get_queryset()
		return super(UserVideoList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserVideoList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['album'] = self.album
		return context

	def get_queryset(self):
		video_list = self.video_list
		return video_list


class UserMusicList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from music.models import SoundList

		self.template_name = request.user.get_template_user(folder="user_music_list/", template="playlist.html", request=request)
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])
		return super(UserMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusicList,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['playlist'] = self.playlist
		return context

	def get_queryset(self):
		playlist = self.playlist.playlist_too()
		return playlist


class AllPossibleUsersList(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = self.user.get_settings_template(folder="u_list/", template="possible_list.html", request=request)
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
		try:
			self.fixed = Post.objects.get(creator__id=user.pk, is_fixed=True)
		except:
			self.fixed = None
		self.user=User.objects.get(pk=self.kwargs["pk"])

		if request.user.is_authenticated:
			if self.user.pk == request.user.pk:
				self.template_name = "lenta/my_list.html"
			elif request.user.is_post_manager():
				self.template_name = "lenta/staff_list.html"
			elif self.user != request.user:
				check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
				if self.user.is_closed_profile():
					check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
				self.template_name = "lenta/list.html"
		elif request.user.is_anonymous:
			if self.user.is_closed_profile():
				raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
			else:
				self.template_name = "lenta/anon_list.html"

		MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + template_name
		return super(PostListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(PostListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['object'] = self.fixed
		return context

	def get_queryset(self):
		posts_list = self.user.get_posts().order_by('-created')
		return posts_list


class AllUsers(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		from common.get_template import get_default_template

		self.template_name = get_default_template(folder="u_list/", template="all_users.html", request=request)
		return super(AllUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		users = User.objects.only("pk")
		return users

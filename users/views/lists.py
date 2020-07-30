import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from users.models import User
from django.views.generic import ListView
from posts.models import Post
from common.template.post import get_permission_user_post
from common.template.video import get_template_user_video
from common.template.music import get_template_user_music


class UserVisitCommunities(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.template_name = request.user.get_settings_template(folder="user_community/", template="visits.html", request=request)
		return super(UserVisitCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		communities = self.request.user.get_visited_communities()
		return communities

class BlackListUsers(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_settings_template(folder="u_list/", template="blacklist.html", request=request)
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

		self.template_name = get_template_user_video(self.user, "user_video_list/", "list.html", request.user)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
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

		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.playlist = SoundList.objects.get(uuid=self.kwargs["uuid"])

		self.template_name = get_template_user_music(self.user, "user_music_list/", "list.html", request.user)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
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

		self.template_name = get_permission_user_post(self.user, "lenta/", "list.html", request.user)
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

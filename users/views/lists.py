from users.models import User
from django.views.generic import ListView
from django.shortcuts import render_to_response
from posts.models import Post


class UserVisitCommunities(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.template_name = request.user.get_settings_template(folder="user_community/", template="visits.html", request=request)
		return super(UserVisitCommunities,self).get(request,*args,**kwargs)

	def get_queryset(self):
		communities = self.request.user.get_visited_communities()
		return communities


class UserVideoList(ListView):
	template_name = None
	paginate_by = 30

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


class AllPossibleUsersList(ListView):
	template_name = None
	model = User
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		from common.utils import is_mobile

		self.user = request.user
		if is_mobile(request):
			self.template_name = "mob_possible_list.html"
		else:
			self.template_name = "possible_list.html"
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
	model = Post
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		try:
			self.fixed = Post.objects.get(creator__id=user.pk, is_fixed=True)
		except:
			self.fixed = None
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_template_list_user(folder="lenta/", template="list.html", request=request)
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
	model = User
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		from common.utils import is_mobile

		if is_mobile(request):
			self.template_name = "mob_all_users.html"
		else:
			self.template_name = "all_users.html"
		return super(AllUsers,self).get(request,*args,**kwargs)

	def get_queryset(self):
		users = User.objects.only("pk")
		return users

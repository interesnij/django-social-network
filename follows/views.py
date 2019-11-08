from django.views import View
from follows.models import Follow
from django.views.generic import ListView
from users.models import User
from django.http import HttpResponse
from communities.models import Community


class FollowsListView(ListView):
	template_name="follows.html"
	model=User
	paginate_by=10

	def get_queryset(self):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		followeds_user=Follow.objects.filter(followed_user=self.user)
		return followeds_user


class FollowCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		new_follow = request.user.follow_user(self.followed_user)
		new_follow.notification_follow(request.user)
		return HttpResponse("!")


class FollowDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		request.user.unfollow_user(self.followed_user)
		return HttpResponse("!")


class CommunityFollowCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		new_follow = request.user.community_follow_user(self.community)
		new_follow.notification_community_follow(request.user)
		return HttpResponse("!")


class CommunityFollowDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		request.user.community_unfollow_user(self.community)
		return HttpResponse("!")

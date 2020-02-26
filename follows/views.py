from django.views import View
from follows.models import Follow
from users.models import User
from django.http import HttpResponse
from communities.models import Community
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from django.views.generic import ListView


class FollowsView(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		return super(FollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FollowsView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		if self.user == self.request.user:
			self.template_name="follows/my_follows.html"
			friends_list=self.user.get_follows()
		elif self.request.user != self.user and self.request.user.is_authenticated:
			if self.request.user.is_blocked_with_user_with_id(user_id=self.user.id):
				self.template_name = "follows/follows_block.html"
			elif self.user.is_closed_profile():
				if not self.request.user.is_connected_with_user_with_id(user_id=self.user.id):
					self.template_name = "follows/close_follows.html"
				else:
					self.template_name = "follows/follows.html"
					friends_list=self.user.get_follows()
			else:
				self.template_name = "follows/follows.html"
				friends_list=self.user.get_follows()
		elif self.request.user.is_anonymous and self.user.is_closed_profile():
			self.template_name = "follows/close_follows.html"
		elif self.request.user.is_anonymous and not self.user.is_closed_profile():
			self.template_name = "follows/anon_follows.html"
			friends_list=self.user.get_follows()
		return friends_list


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
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		new_follow = self.user.community_follow_user(self.community)
		new_follow.notification_community_follow(self.user)
		return HttpResponse("!")


class CommunityFollowDelete(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		self.user.community_unfollow_user(self.community)
		return HttpResponse("!")

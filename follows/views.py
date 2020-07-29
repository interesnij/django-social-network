import re
MOBILE_AGENT_RE = re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
from communities.models import Community
from django.views import View
from follows.models import Follow
from users.models import User
from django.http import HttpResponse
from django.views.generic import ListView


class FollowsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])

		self.template_name = self.user.get_template_user("follows/", "follows.html", request.user)
		if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
			self.template_name = "mob_" + self.template_name
		return super(FollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FollowsView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		friends_list = self.user.get_followers()
		return friends_list

class FollowingsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user = request.user
		self.template_name = self.user.get_settings_template(folder="follows/", template="followings.html", request=request)
		return super(FollowingsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FollowingsView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		possible_list = self.user.get_followings()
		return possible_list


class FollowCreate(View):
	def get(self,request,*args,**kwargs):
		followed_user = User.objects.get(pk=self.kwargs["pk"])
		new_follow = request.user.follow_user(followed_user)
		request.user.notification_follow(followed_user)
		return HttpResponse("!")

class FollowView(View):
	def get(self,request,*args,**kwargs):
		follow_user = User.objects.get(pk=self.kwargs["pk"])
		try:
			follow = Follow.objects.get(user=follow_user, followed_user=request.user)
			follow.view = True
			follow.save(update_fields=['view'])
		except:
			pass
		return HttpResponse("!")


class FollowDelete(View):
	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		request.user.unfollow_user(self.followed_user)
		return HttpResponse("!")


class CommunityFollowCreate(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		new_follow = request.user.community_follow_user(self.community)
		self.community.notification_community_follow(request.user)
		return HttpResponse("!")


class CommunityFollowDelete(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		request.user.community_unfollow_user(self.community)
		return HttpResponse("!")


class CommunityFollowView(View):
	def get(self,request,*args,**kwargs):
		community = Community.objects.get(pk=self.kwargs["pk"])
		user = User.objects.get(uuid=self.kwargs["uuid"])
		follow = CommunityFollow.objects.get(user=user, community=community)
		follow.view = True
		follow.save(update_fields=['view']) 
		return HttpResponse("!")

from django.views import View
from follows.models import Follow
from users.models import User
from django.http import HttpResponse
from django.views.generic import ListView


class FollowsView(ListView):
	template_name = None
	paginate_by = 15

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_template_user(folder="follows/", template="follows.html", request=request)
		return super(FollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FollowsView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		friends_list=self.user.get_followers()
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
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		new_follow = request.user.follow_user(self.followed_user)
		new_follow.notification_follow(request.user)
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
		from communities.models import Community

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		new_follow = self.user.community_follow_user(self.community)
		new_follow.notification_community_follow(self.user)
		return HttpResponse("!")


class CommunityFollowDelete(View):
	def get(self,request,*args,**kwargs):
		from communities.models import Community

		self.community = Community.objects.get(pk=self.kwargs["pk"])
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		self.user.community_unfollow_user(self.community)
		return HttpResponse("!")

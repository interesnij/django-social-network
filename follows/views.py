from communities.models import Community
from django.views import View
from follows.models import Follow, CommunityFollow
from users.models import User
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from common.templates import get_settings_template, get_template_user, get_template_anon_user


class FollowsView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			self.template_name = get_template_user(self.user, "follows/", "follows.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user(self.user, "follows/anon_follows.html", request.META['HTTP_USER_AGENT'])
		return super(FollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FollowsView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		friends_list = self.user.get_followers()
		return friends_list

class FollowingsView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.template_name = get_settings_template("follows/followings.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(FollowingsView,self).get(request,*args,**kwargs)

	def get_queryset(self):
		return self.request.user.get_followings()


class FollowCreate(View):
	def get(self,request,*args,**kwargs):
		from common.notify.notify import user_notify

		followed_user = User.objects.get(pk=self.kwargs["pk"])
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
			new_follow = request.user.follow_user(followed_user)
			user_notify(request.user, None, followed_user.pk, "USE", "u_follow", "CRE")
			return HttpResponse()
		else:
			raise Http404

class FollowView(View):
	def get(self,request,*args,**kwargs):
		follow_user = User.objects.get(pk=self.kwargs["pk"])
		try:
			if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
				follow = Follow.objects.get(user=follow_user, followed_user=request.user)
				follow.view = True
				follow.save(update_fields=['view'])
				return HttpResponse()
			else:
				raise Http404
		except:
			pass

class FollowDelete(View):
	def get(self,request,*args,**kwargs):
		self.followed_user = User.objects.get(pk=self.kwargs["pk"])
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
			request.user.unfollow_user(self.followed_user)
			return HttpResponse()
		else:
			raise Http404

class CommunityFollowCreate(View):
	def get(self,request,*args,**kwargs):
		from common.notify.notify import community_notify

		community = Community.objects.get(pk=self.kwargs["pk"])
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
			new_follow = request.user.community_follow_user(community)
			community_notify(request.user, community, None, "no", "c_follow", "CRE")
			return HttpResponse()
		else:
			raise Http404


class CommunityFollowDelete(View):
	def get(self,request,*args,**kwargs):
		self.community = Community.objects.get(pk=self.kwargs["pk"])
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
			request.user.community_unfollow_user(self.community)
			return HttpResponse("!")
		else:
			raise Http404

class CommunityFollowView(View):
	def get(self,request,*args,**kwargs):
		community, user = Community.objects.get(pk=self.kwargs["pk"]), User.objects.get(uuid=self.kwargs["uuid"])
		try:
			if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
				follow = CommunityFollow.objects.get(user=user, community=community)
				follow.view = True
				follow.save(update_fields=['view'])
				return HttpResponse("!")
			else:
				raise Http404
		except:
			pass

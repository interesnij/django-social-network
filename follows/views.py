from django.views import View
from django.views.generic.base import TemplateView
from follows.models import Follow
from users.models import User
from django.http import HttpResponse
from communities.models import Community
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class FollowsView(TemplateView):
	template_name = None
	featured_users = None

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		self.request_user = request.user

		if self.user == request.user:
			self.template_name="follows/my_follows.html"
			self.featured_users = request.user.get_possible_friends2()[0:10]
		elif request.user != self.user and request.user.is_authenticated:
			if request.user.is_blocked_with_user_with_id(user_id=self.user.id):
				self.template_name = "follows/follows_block.html"
			elif self.user.is_closed_profile():
				if not request.user.is_connected_with_user_with_id(user_id=self.user.id):
					self.template_name = "follows/close_follows.html"
				else:
					self.template_name = "follows/follows.html"
					self.featured_users = request.user.get_possible_friends2()
			else:
				self.template_name = "follows/follows.html"
				self.featured_users = request.user.get_possible_friends2()
		elif request.user.is_anonymous and self.user.is_closed_profile():
			self.template_name = "follows/close_follows.html"
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			self.template_name = "follows/anon_follows.html"
		return super(FollowsView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FollowsView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['featured_users'] = self.featured_users
		return context


class FollowsListView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        self.user=User.objects.get(uuid=self.kwargs["uuid"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            follows_list=self.user.get_follows()
            current_page = Paginator(follows_list, 1)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            follows_list=self.user.get_follows()
            current_page = Paginator(follows_list, 1)
        elif self.user == request.user:
            follows_list=self.user.get_follows()
            current_page = Paginator(follows_list, 1)
        context['user'] = self.user
        page = request.GET.get('page')
        try:
            context['follows_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['follows_list'] = current_page.page(1)
        except EmptyPage:
            context['follows_list'] = current_page.page(current_page.num_pages)
        return render_to_response('follows.html', context)



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

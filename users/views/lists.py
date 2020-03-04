from users.models import User
from django.views.generic import ListView
from django.shortcuts import render_to_response
from main.models import Item
from communities.models import Community


class UserCommunitiesList(ListView):
	template_name = None
	model = Community
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		self.popular_list = Community.get_trending_communities_for_user_with_id(user_id=self.user.pk)
		self.template_name = self.user.get_permission_list_user(folder="user_community/", template="communities_list.html", request=request)
		communities_list = Community.objects.filter(memberships__user__id=self.user.pk)
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = self.user.get_template_list_user(folder="user_community/", template="list.html", request=request)
		return super(UserCommunitiesList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserCommunitiesList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		communities_list = Community.objects.filter(memberships__user__id=self.user.pk)
		return communities_list


class UserManageCommunitiesList(ListView):
	template_name = None
	model = Community
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		if self.user == request.user:
			self.template_name = "user_community/communities_list_with_staffed.html"
		else:
			self.template_name = "main/auth.html"
		communities_list = Community.objects.filter(memberships__user__id=self.user.pk)
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		return super(UserManageCommunitiesList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserManageCommunitiesList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		manage_communities_list = self.user.get_staffed_communities()
		return manage_communities_list


class UserMusicList(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = self.user.get_permission_list_user(folder="user_music/", template="list.html", request=request)
		return super(UserMusicList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserMusicList,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		music_list = list(reversed(self.user.get_music()))
		return music_list

class AllPossibleUsersList(ListView):
	template_name = None
	model = User
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		from common.utils import is_mobile

		self.user = User.objects.get(uuid=self.kwargs["uuid"])
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
		if self.request.user.is_authenticated:
			possible_list = request.user.get_possible_friends()
		else:
			possible_list = None
		return possible_list

class ItemListView(ListView):
	template_name = None
	model = Item
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		try:
			self.fixed = Item.objects.get(creator__id=user.pk, is_fixed=True)
		except:
			self.fixed = None
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.template_name = self.user.get_template_list_user(folder="lenta/", template="list.html", request=request)
		return super(ItemListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ItemListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['object'] = self.fixed
		return context

	def get_queryset(self):
		items_list = self.user.get_posts().order_by('-created')
		return items_list


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

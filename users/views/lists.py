from users.models import User
from django.views.generic import ListView
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from common.utils import is_mobile
from main.models import Item


class UserCommunitiesList(View):
	def get(self, request, *args, **kwargs):
		from main.models import Item
		from communities.models import Community

		context = {}
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		popular_list = Community.get_trending_communities_for_user_with_id(user_id=self.user.pk)
		template = self.user.get_permission_list_user(folder="user_community/", template="communities_list.html", request=request)
		communities_list = Community.objects.filter(memberships__user__id=self.user.pk)
		current_page = Paginator(communities_list, 30)
		page = request.GET.get('page')
		context['user'] = self.user
		try:
			context['communities_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['communities_list'] = current_page.page(1)
		except EmptyPage:
			context['communities_list'] = current_page.page(current_page.num_pages)
		return render_to_response(template, context)


class UserManageCommunitiesList(View):
	def get(self, request, *args, **kwargs):
		context = {}
		template = "user_community/communities_list_with_staffed.html"
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		if self.user ==request.user:
			manage_communities_list = self.user.get_staffed_communities()
		else:
			manage_communities_list = ""
		current_page = Paginator(manage_communities_list, 30)
		page = request.GET.get('page')
		context['user'] = self.user
		try:
			context['manage_communities_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['manage_communities_list'] = current_page.page(1)
		except EmptyPage:
			context['manage_communities_list'] = current_page.page(current_page.num_pages)
		return render_to_response(template, context)


class UserMusicList(View):
	def get(self, request, *args, **kwargs):
		context = {}
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		template = self.user.get_permission_list_user(folder="user_music/", template="list.html", request=request)
		current_page = Paginator(music_list, 30)
		page = request.GET.get('page')
		context['user'] = self.user
		context['request_user'] = request.user
		try:
			context['music_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['music_list'] = current_page.page(1)
		except EmptyPage:
			context['music_list'] = current_page.page(current_page.num_pages)
		return render_to_response(template, context)


class AllPossibleUsersList(View):
	def get(self, request, *args, **kwargs):
		context = {}
		if request.user.is_authenticated:
			possible_list = request.user.get_possible_friends()
			current_page = Paginator(possible_list, 30)
			page = request.GET.get('page')
		else:
			possible_list = None
		context['request_user'] = request.user

		try:
			context['possible_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['possible_list'] = current_page.page(1)
		except EmptyPage:
			context['possible_list'] = current_page.page(current_page.num_pages)
		return render_to_response('possible_list.html', context)

class ItemListView(ListView):
	template_name = None
	model = Item
	paginate_by = 2

	def get(self,request,*args,**kwargs):
		try:
			self.fixed = Item.objects.get(creator__id=user.pk, is_fixed=True)
		except:
			self.fixed = None
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.template = user.get_template_list_user(folder="lenta/", template="list.html", request=request)
		return super(ItemListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(ItemListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['object'] = self.fixed
		return context

	def get_queryset(self):
		items_list = user.get_posts().order_by('-created')
		return items_list

class ItemListView2(View):
	def get(self, request, *args, **kwargs):
		from main.models import Item

		context = {}
		template = None
		user=User.objects.get(pk=self.kwargs["pk"])
		try:
			fixed = Item.objects.get(creator__id=user.pk, is_fixed=True)
		except:
			fixed = None
		template = user.get_template_list_user(folder="lenta/", template="list.html", request=request)
		items_list = user.get_posts().order_by('-created')
		current_page = Paginator(items_list, 30)
		context['request_user'] = request.user
		context['user'] = user
		context['object'] = fixed
		page = request.GET.get('page')
		try:
			context['items_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['items_list'] = current_page.page(1)
		except EmptyPage:
			context['items_list'] = current_page.page(current_page.num_pages)

		return render_to_response(template, context)


class AllUsers(ListView):
	template_name="all_users.html"
	model=User
	paginate_by=30

	def get_queryset(self):
		items = User.objects.only("pk")
		return items

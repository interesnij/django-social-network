from users.models import User
from communities.models import Community
from django.views.generic import ListView
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from main.models import Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied


class UserCommunitiesList(View):
	def get(self, request, *args, **kwargs):
		context = {}
		template = None
		self.user=User.objects.get(uuid=self.kwargs["uuid"])
		if self.user != request.user and request.user.is_authenticated:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile():
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
			communities_list = Community.objects.filter(memberships__user__id=self.user.pk).order_by('-created')
			template = 'user_community/communities_list.html'
			current_page = Paginator(communities_list, 12)
		elif request.user.is_anonymous and self.user.is_closed_profile():
			raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			communities_list = Community.objects.filter(memberships__user__id=self.user.pk).order_by('-created')
			template = 'user_community/communities_list.html'
			current_page = Paginator(communities_list, 12)
		elif self.user == request.user:
			communities_list = Community.objects.filter(memberships__user__id=self.user.pk).order_by('-created')
			template = 'user_community/communities_list.html'
			current_page = Paginator(communities_list, 12)
		page = request.GET.get('page')
		context['user'] = self.user
		try:
			context['communities_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['communities_list'] = current_page.page(1)
		except EmptyPage:
			context['communities_list'] = current_page.page(current_page.num_pages)
		return render_to_response(template, context)


class AllUsersList(View):
	def get(self, request, *args, **kwargs):
		context = {}
		users_list = User.objects.only('pk')
		current_page = Paginator(users_list, 12)
		page = request.GET.get('page')

		try:
			context['users_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['users_list'] = current_page.page(1)
		except EmptyPage:
			context['users_list'] = current_page.page(current_page.num_pages)
		return render_to_response('all_users_list.html', context)


class AllPossibleUsersList(View):
	def get(self, request, *args, **kwargs):
		context = {}
		if request.user.is_authenticated:
			possible_list = request.user.get_possible_friends()
			current_page = Paginator(possible_list, 12)
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


class ItemListView(View):
	def get(self, request, *args, **kwargs):
		context = {}
		template = None
		self.user=User.objects.get(pk=self.kwargs["pk"])
		fixed = Item.objects.get(user__id=self.user.pk, is_fixed=True)
		if self.user != request.user and request.user.is_authenticated:
			check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
			if self.user.is_closed_profile():
				check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
			items_list = self.user.get_posts().order_by('-created')
			template = 'lenta/item_list.html'
			current_page = Paginator(items_list, 10)
		elif request.user.is_anonymous and self.user.is_closed_profile():
			raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			items_list = self.user.get_posts().order_by('-created')
			template = 'lenta/item_list_anon.html'
			current_page = Paginator(items_list, 10)
		elif self.user == request.user:
			items_list = self.user.get_posts().order_by('-created')
			template = 'lenta/my_item_list.html'
			current_page = Paginator(items_list, 10)

		context['user'] = self.user
		context['object'] = fixed
		page = request.GET.get('page')
		try:
			context['items_list'] = current_page.page(page)
		except PageNotAnInteger:
			context['items_list'] = current_page.page(1)
		except EmptyPage:
			context['items_list'] = current_page.page(current_page.num_pages)

		return render_to_response(template, context)

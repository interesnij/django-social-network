from django.views.generic.base import TemplateView
from users.models import User
from django.views import View
from django.http import HttpResponse
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


class FrendsListView(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		try:
			self.featured_users = request.user.get_possible_friends()[0:10]
		except:
			self.featured_users = None
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FrendsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['featured_users'] = self.featured_users
		return context

	def get_queryset(self):
		if self.user == self.request.user:
			self.template_name="frends/my_frends.html"
			friends_list=self.user.get_all_connection()
		elif self.request.user != self.user and self.request.user.is_authenticated:
			if self.request.user.is_blocked_with_user_with_id(user_id=self.user.id):
				self.template_name = "frends/frends_block.html"
			elif self.user.is_closed_profile():
				if not self.request.user.is_connected_with_user_with_id(user_id=self.user.id):
					self.template_name = "frends/close_frends.html"
				else:
					self.template_name = "frends/frends.html"
					friends_list=self.user.get_all_connection()
			else:
				self.template_name = "frends/frends.html"
				friends_list=self.user.get_all_connection()
		elif self.request.user.is_anonymous and self.user.is_closed_profile():
			self.template_name = "frends/close_frends.html"
		elif self.request.user.is_anonymous and not self.user.is_closed_profile():
			self.template_name = "frends/anon_frends.html"
			friends_list=self.user.get_all_connection()
		return friends_list

class OnlineFrendsListView(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.featured_users = request.user.get_possible_friends()[0:10]
		return super(OnlineFrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(OnlineFrendsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['featured_users'] = self.featured_users
		return context

	def get_queryset(self):
		if self.user == self.request.user:
			self.template_name="frends_online/my_frends.html"
			friends_list=self.user.get_online_connection()
		elif self.request.user != self.user and self.request.user.is_authenticated:
			if self.request.user.is_blocked_with_user_with_id(user_id=self.user.id):
				self.template_name = "frends_online/frends_block.html"
			elif self.user.is_closed_profile():
				if not self.request.user.is_connected_with_user_with_id(user_id=self.user.id):
					self.template_name = "frends_online/close_frends.html"
				else:
					self.template_name = "frends_online/frends.html"
					friends_list=self.user.get_online_connection()
			else:
				self.template_name = "frends_online/frends.html"
				friends_list=self.user.get_online_connection()
		elif self.request.user.is_anonymous and self.user.is_closed_profile():
			self.template_name = "frends_online/close_frends.html"
		elif self.request.user.is_anonymous and not self.user.is_closed_profile():
			self.template_name = "frends_online/anon_frends.html"
			friends_list=self.user.get_online_connection()
		return friends_list

class CommonFrendsListView(ListView):
	template_name = None
	paginate_by = 30

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.featured_users = request.user.get_possible_friends()[0:10]
		return super(CommonFrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommonFrendsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['featured_users'] = self.featured_users
		return context

	def get_queryset(self):
		if self.request.user != self.user and self.request.user.is_authenticated:
			if self.request.user.is_blocked_with_user_with_id(user_id=self.user.id):
				self.template_name = "frends_common/frends_block.html"
			elif self.user.is_closed_profile():
				if not self.request.user.is_connected_with_user_with_id(user_id=self.user.id):
					self.template_name = "frends_common/close_frends.html"
				else:
					self.template_name = "frends_common/frends.html"
					friends_list=self.user.get_common_friends_of_user(self.request.user)
			else:
				self.template_name = "frends_common/frends.html"
				friends_list=self.user.get_common_friends_of_user(self.request.user)
		return friends_list


class ConnectCreate(View):
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])
		new_frend = request.user.frend_user(self.target_user)
		new_frend.notification_connect(request.user)
		return HttpResponse("!")


class ConnectDelete(View):
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])
		request.user.unfrend_user(self.target_user)
		return HttpResponse("!")

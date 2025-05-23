from users.models import User
from django.views import View
from django.http import HttpResponse, Http404
from django.views.generic import ListView
from common.templates import get_template_user, get_settings_template, get_template_anon_user


class FrendsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			self.template_name = get_template_user(self.user, "frends/frends/", "frends.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user(self.user, "frends/frends/anon_frends.html", request.META['HTTP_USER_AGENT'])
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(FrendsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		friends_list = self.user.get_all_friends()
		return friends_list

class OnlineFrendsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		if request.user.is_authenticated:
			self.template_name = get_template_user(self.user, "frends/frends_online/", "frends.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_anon_user(self.user, "frends/frends_online/anon_frends.html", request.META['HTTP_USER_AGENT'])
		return super(OnlineFrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(OnlineFrendsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		friends_list = self.user.get_online_friends()
		return friends_list

class CommonFrendsListView(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("frends/frends_common/frends.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommonFrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CommonFrendsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

	def get_queryset(self):
		friends_list = self.user.get_common_friends_of_user(self.request.user)
		return friends_list


class ConnectCreate(View):
	def get(self,request,*args,**kwargs):
		from common.notify.notify import user_notify

		target_user = User.objects.get(pk=self.kwargs["pk"])
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
			new_frend = request.user.frend_user(target_user)
			user_notify(request.user, None, target_user.pk, "USE", "u_connect_create", "CCO")
			return HttpResponse()
		else:
			raise Http404

class ConnectDelete(View):
	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])
		if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
			request.user.unfrend_user(self.target_user)
			return HttpResponse("")
		else:
			raise Http404

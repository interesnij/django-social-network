from django.views.generic.base import TemplateView
from users.models import User
from django.views import View
from django.http import HttpResponse
from common.checkers import check_is_not_blocked_with_user_with_id, check_is_connected_with_user_with_id
from django.shortcuts import render_to_response
from rest_framework.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class FrendsListView(TemplateView):
	template_name = None
	featured_users = None

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(uuid=self.kwargs["uuid"])

		if self.user == request.user:
			self.template_name="frends/my_frends.html"
		elif request.user != self.user and request.user.is_authenticated:
			if request.user.is_blocked_with_user_with_id(user_id=self.user.id):
				self.template_name = "frends/frends_block.html"
			elif self.user.is_closed_profile():
				if not request.user.is_connected_with_user_with_id(user_id=self.user.id):
					self.template_name = "frends/close_frends.html"
				else:
					self.template_name = "frends/frends.html"
					self.common_frends = self.user.get_common_friends_of_user(request.user)[0:5]
					self.featured_users = request.user.get_possible_friends2()[0:10]
			else:
				self.template_name = "frends/frends.html"
				self.featured_users = request.user.get_possible_friends2()[0:10]
		elif request.user.is_anonymous and self.user.is_closed_profile():
			self.template_name = "frends/close_frends.html"
		elif request.user.is_anonymous and not self.user.is_closed_profile():
			self.template_name = "frends/anon_frends.html"
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FrendsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['featured_users'] = self.featured_users
		return context


class AllFrendsListView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            frends_list=self.user.get_all_connection()
            current_page = Paginator(frends_list, 12)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            frends_list=self.user.get_all_connection()
            current_page = Paginator(frends_list, 12)
        elif self.user == request.user:
            frends_list=self.user.get_all_connection()
            current_page = Paginator(frends_list, 12)
        context['user'] = self.user
        context['request_user'] = request.user
        page = request.GET.get('page')
        try:
            context['frends_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['frends_list'] = current_page.page(1)
        except EmptyPage:
            context['frends_list'] = current_page.page(current_page.num_pages)
        return render_to_response('frends_list.html', context)


class OnlineFrendsListView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            online_list=self.user.get_pop_online_connection()
            current_page = Paginator(online_list, 12)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            online_list=self.user.get_pop_online_connection()
            current_page = Paginator(online_list, 12)
        elif self.user == request.user:
            online_list=self.user.get_pop_online_connection()
            current_page = Paginator(online_list, 12)
        context['user'] = self.user
        context['request_user'] = request.user
        page = request.GET.get('page')
        try:
            context['online_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['online_list'] = current_page.page(1)
        except EmptyPage:
            context['online_list'] = current_page.page(current_page.num_pages)
        return render_to_response('online_frends_list.html', context)


class CommonFrendsListView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        self.user=User.objects.get(pk=self.kwargs["pk"])
        if self.user != request.user and request.user.is_authenticated:
            check_is_not_blocked_with_user_with_id(user=request.user, user_id=self.user.id)
            if self.user.is_closed_profile():
                check_is_connected_with_user_with_id(user=request.user, user_id=self.user.id)
            common_list = request.user.get_common_friends_of_user(self.user)
            current_page = Paginator(common_list, 10)
        elif request.user.is_anonymous and self.user.is_closed_profile():
            raise PermissionDenied('Это закрытый профиль. Только его друзья могут видеть его информацию.')
        elif request.user.is_anonymous and not self.user.is_closed_profile():
            common_list = request.user.get_common_friends_of_user(self.user)
            current_page = Paginator(common_list, 12)
        elif self.user == request.user:
            common_list = request.user.get_common_friends_of_user(self.user)
            current_page = Paginator(common_list, 12)
        context['user'] = self.user
        context['request_user'] = request.user
        page = request.GET.get('page')
        try:
            context['common_list'] = current_page.page(page)
        except PageNotAnInteger:
            context['common_list'] = current_page.page(1)
        except EmptyPage:
            context['common_list'] = current_page.page(current_page.num_pages)
        return render_to_response('common_frends_list.html', context)


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

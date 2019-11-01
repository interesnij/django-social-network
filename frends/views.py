from django.views.generic import ListView
from users.models import User
from django.views import View
from django.http import HttpResponse
from frends.models import Connect
from follows.models import Follow
from django.db.models import Q


class FrendsListView(ListView):
	template_name="frends.html"
	model=User

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.all_frends = Connect.objects.filter(Q(user=self.user)|Q(target_user=self.user))
		self.featured_users = User.objects.all()
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FrendsListView,self).get_context_data(**kwargs)
		context['all_frends'] = self.all_frends
		context['featured_users'] = self.featured_users
		context['user'] = self.user
		return context


class ConnectCreate(View):
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])

		new_frend = request.user.frend_user(self.target_user)
		new_follow.notification_connect(request.user)
		return HttpResponse("!")


class ConnectDelete(View):
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])
		request.user.unfrend_user(self.target_user)
		return HttpResponse("!")

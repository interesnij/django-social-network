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
	paginate_by=10

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.featured_users = request.user.get_possible_friends()[0:10]
		self.common_frends = request.user.get_common_friends_of_user(self.user)
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FrendsListView,self).get_context_data(**kwargs)
		context['featured_users'] = self.featured_users
		context['common_frends'] = self.common_frends
		context['user'] = self.user
		return context

	def get_queryset(self):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		frends=self.user.get_all_connection()
		return frends


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

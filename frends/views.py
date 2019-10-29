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
		try:
			self.connect = Connect.objects.get(target_user=self.target_user,user=request.user)
		except:
			self.connect = None
		if not self.connect and self.target_user != request.user:
			Connect.create_connection(user_id=request.user.id, target_user_id=self.target_user.id)
			fol=Follow.objects.get(user=self.target_user, followed_user=request.user)
			fol.delete()
		else:
			return HttpResponse("Пользователь уже с Вами дружит :-)")
		return HttpResponse("!")


class ConnectDelete2(View):
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.connect = Connect.objects.get(target_user=self.target_user,user=self.request.user)
		except:
			self.connect = None
		if self.connect and self.target_user != request.user:
			conn = Connect.objects.get(target_user=self.target_user, user=request.user)
			conn.delete()
			Follow.objects.create(user=self.target_user, followed_user=request.user)
		else:
			return HttpResponse("Пользователь уже удален :-)")
		return HttpResponse("!")

class ConnectDelete(View):
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.connect = Connect.objects.get(target_user=request.user,user=self.user)
		except:
			self.connect = None
		if self.connect and self.user != request.user:
			conn = Connect.objects.get(target_user=request.user, user=self.user)
			conn.delete()
			Follow.objects.create(user=self.user, followed_user=request.user)
		else:
			return HttpResponse("Пользователь уже удален :-)")
		return HttpResponse("!")

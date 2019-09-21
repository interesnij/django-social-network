from django.views.generic import ListView
from users.models import User
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from frends.models import Connect
from follows.models import Follow


class FrendsListView(ListView):
	template_name="frends.html"
	model=User

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.frends_users=Connect.objects.filter(user=self.user)
		self.target_users=Connect.objects.filter(target_user=self.user)
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FrendsListView,self).get_context_data(**kwargs)
		context["frends_users"]=self.frends_users
		context['target_users'] = self.target_users
		context['user'] = self.user
		return context


class ConnectCreate(TemplateView):
	template_name = "connect_add.html"
	success_url = "/"
	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.connect = Connect.objects.get(target_user=self.target_user,user=request.user)
		except:
			self.connect = None
		if not self.connect and self.target_user != request.user:
			Connect.create_connection(target_user=self.target_user,user=request.user)
			fol=Follow.objects.get(user=self.target_user, followed_user=request.user)
			fol.delete()
		else:
			return HttpResponse("Пользователь уже с Вами дружит :-)")
		return super(ConnectCreate,self).get(request,*args,**kwargs)


class ConnectDelete(TemplateView):
	template_name = "connect_delete.html"
	success_url = "/"

	def get(self,request,*args,**kwargs):
		self.target_user = User.objects.get(pk=self.kwargs["pk"])
		try:
			self.connect = Connect.objects.get(target_user=self.target_user,user=request.user)
		except:
			self.connect = None
		if self.connect and self.target_user != request.user:
			conn=Connect.objects.get(target_user=self.target_user, user=request.user)
			conn.delete()
			Follow.objects.create(user=self.target_user, followed_user=request.user)
		else:
			return HttpResponse("Пользователь уже с Вами дружит :-)")
		return super(ConnectCreate,self).get(request,*args,**kwargs)

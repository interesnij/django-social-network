from django.views.generic import ListView
from users.models import User
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from frends.models import Connect
from follows.models import Follow


class FrendsListView(ListView):
	template_name="frends.html"
	model=User

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.frends=Connection.objects.filter(target_connection__user=self.user)
		self.frends2=Connection.objects.filter(target_connection__target_user=self.user)
		self.all_user=User.objects.all()
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FrendsListView,self).get_context_data(**kwargs)
		context["frends"]=self.frends
		context['frends2'] = self.frends2
		context['user'] = self.user
		context['all_user'] = self.all_user
		return context


class ConnectCreate(TemplateView):
    template_name = "connect_add.html"
    success_url = "/"

    def get(self,request,*args,**kwargs):
        self.user=request.user
        self.target_user = Follow.objects.get(pk=self.kwargs["pk"])
        try:
            self.connect = Connect.objects.get(target_user=self.target_user,user=self.user)
        except:
            self.connect = None

        if not self.connect and self.target_user != self.user:
            Connect.objects.create(target_user=self.target_user, user=self.user)
        else:
            return HttpResponse("Пользователь уже с Вами дружит :-)")
        return super(ConnectCreate,self).get(request,*args,**kwargs)


class ConnectDelete(TemplateView):
    template_name = "connect_delete.html"
    success_url = "/"

    def get(self,request,*args,**kwargs):
        self.user=request.user
        self.target_user = Follow.objects.get(pk=self.kwargs["pk"])
        try:
            self.connect = Connect.objects.get(target_user=self.target_user,user=self.user)
        except:
            self.connect = None

        if self.connect and self.target_user != self.user:
            Connect.objects.delete(target_user=self.target_user, user=self.user)
        else:
            return HttpResponse("Пользователь уже с Вами дружит :-)")
        return super(ConnectCreate,self).get(request,*args,**kwargs)

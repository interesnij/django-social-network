from django.views.generic import ListView
from users.models import User
from connections.models import Connection


class FrendsListView(ListView):
	template_name="frends.html"
	model=User
	all_user=User.objects.all()

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.frends=Connection.objects.filter(target_connection__user=self.user)
		self.frends2=Connection.objects.filter(target_connection__target_user=self.user)
		return super(FrendsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(FrendsListView,self).get_context_data(**kwargs)
		context["frends"]=self.frends
		context['frends2'] = self.frends2
		context['user'] = self.user
		context['all_user'] = all_user
		return context

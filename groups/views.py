from django.views.generic import ListView
from users.models import User


class GroupsListView(ListView):
	template_name="frends.html"
	model=User

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		return super(GroupsListView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(GroupsListView,self).get_context_data(**kwargs)
		context['user'] = self.user
		return context

from django.views.generic import ListView
from users.models import User
from communities.models import Community


class CommunitiesView(ListView):
	template_name="connections.html"
	model=Community

	def get(self,request,*args,**kwargs):
		self.user=User.objects.get(pk=self.kwargs["pk"])
		self.groups=Community.objects.filter(memberships__user=self.user)
		return super(CommunitiesView,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context=super(CommunitiesView,self).get_context_data(**kwargs)
		context["groups"]=self.groups
		context['user'] = self.user
		return context

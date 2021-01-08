from users.models import User
from django.views.generic import ListView
from docs.models import DocList
from common.template.doc import get_template_user_doc


class UserLoadDoclist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.user = User.objects.get(pk=self.kwargs["pk"])
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		self.template_name = get_template_user_doc(self.list, "docs/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserLoadDoclist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserLoadDoclist,self).get_context_data(**kwargs)
		context['user'] = self.user
		context['list'] = self.list
		return context

	def get_queryset(self):
		list = self.list.get_docs()
		return list

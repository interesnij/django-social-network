from communities.models import Community
from django.views.generic import ListView
from docs.models import DocList
from common.template.doc import get_template_community_doc, get_template_user_doc


class CommunityLoadDoclist(ListView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.c, self.list = Community.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
		if self.list.community:
			self.template_name = get_template_community_doc(self.list, "docs/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			self.template_name = get_template_user_doc(self.list, "docs/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(CommunityLoadDoclist,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		c = super(CommunityLoadDoclist,self).get_context_data(**kwargs)
		c['community'], c['list'] = self.c, self.list
		return c

	def get_queryset(self):
		list = self.list.get_items()
		return list

from docs.models import Doclist, Doc
from django.views.generic import ListView


class DocsView(ListView):
	template_name = "docs.html"

	def get_queryset(self):
		return Doc.objects.only("pk")


class LoadDocList(ListView):
	template_name, community = None, None

	def get(self,request,*args,**kwargs):
		self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
		if self.list.community:
			from common.templates import get_template_community_item, get_template_anon_community_item
			self.community = self.list.community
			if request.user.is_authenticated:
				self.template_name = get_template_community_item(self.list, "docs/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_community_item(self.list, "docs/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		else:
			from common.templates import get_template_user_item, get_template_anon_user_item

			if request.user.is_authenticated:
				self.template_name = get_template_user_item(self.list, "docs/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			else:
				self.template_name = get_template_anon_user_item(self.list, "docs/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(LoadDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadDocList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.community
		return context

	def get_queryset(self):
		return self.list.get_items()

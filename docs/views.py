from docs.models import DocsList, Doc
from django.views.generic import ListView
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
							)

class DocsView(ListView):
	template_name = "docs.html"

	def get_queryset(self):
		return Doc.objects.only("pk")


class LoadDocList(ListView):
	template_name, c, paginate_by, is_user_can_see_doc_section, is_user_can_see_doc_list, is_user_can_create_docs = None, None, 10, None, None, None

	def get(self,request,*args,**kwargs):
		self.list = DocsList.objects.get(pk=self.kwargs["pk"])
		if self.list.community:
			self.c = self.list.community
			if request.user.is_authenticated:
				if request.user.is_staff_of_community(self.c.pk):
					self.get_lists = DocsList.get_community_staff_lists(self.c.pk)
					self.is_user_can_see_doc_section = True
					self.is_user_can_create_docs = True
					self.is_user_can_see_doc_list = True
					self.template_name = get_template_community_list(self.list, "docs/community/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
				else:
					self.get_lists = DocsList.get_community_lists(self.c.pk)
					self.is_user_can_see_doc_section = self.c.is_user_can_see_doc(request.user.pk)
					self.is_user_can_see_doc_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_docs = self.list.is_user_can_create_el(request.user.pk)
			elif request.user.is_anonymous:
				self.template_name = get_template_anon_community_list(self.list, "docs/community/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_doc_section = self.c.is_anon_user_can_see_doc()
				self.is_user_can_see_doc_list = self.list.is_anon_user_can_see_el()
				self.get_lists = DocsList.get_community_lists(self.c.pk)
		else:
			if request.user.is_authenticated:
				if request.user.pk == self.list.creator.pk:
					user = self.list.creator
					self.is_user_can_see_doc_section = True
					self.is_user_can_see_doc_list = True
					self.is_user_can_create_docs = True
				else:
					self.is_user_can_see_doc_section = user.is_user_can_see_doc(request.user.pk)
					self.is_user_can_see_doc_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_docs = self.list.is_user_can_create_el(request.user.pk)
				self.template_name = get_template_user_list(self.list, "docs/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "docs/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_doc_section = self.user.is_anon_user_can_see_doc()
				self.is_user_can_see_doc_list = self.list.is_anon_user_can_see_el()
		return super(LoadDocList,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(LoadDocList,self).get_context_data(**kwargs)
		context["list"] = self.list
		context["community"] = self.c
		context['is_user_can_see_doc_section'] = self.is_user_can_see_doc_section
		context['is_user_can_see_doc_list'] = self.is_user_can_see_doc_list
		context['is_user_can_create_docs'] = self.is_user_can_create_docs
		return context

	def get_queryset(self):
		return self.list.get_items()

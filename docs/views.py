from docs.models import DocsList, Doc
from django.views import View
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from common.templates import (
								get_template_community_item,
								get_template_anon_community_item,
								get_template_user_item,
								get_template_anon_user_item,
								get_template_community_list,
								get_template_anon_community_list,
								get_template_user_list,
								get_template_anon_user_list,
								get_settings_template
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
					creator = self.list.creator
					self.is_user_can_see_doc_section = True
					self.is_user_can_see_doc_list = True
					self.is_user_can_create_docs = True
				else:
					self.is_user_can_see_doc_section = creator.is_user_can_see_doc(request.user.pk)
					self.is_user_can_see_doc_list = self.list.is_user_can_see_el(request.user.pk)
					self.is_user_can_create_docs = self.list.is_user_can_create_el(request.user.pk)
				self.template_name = get_template_user_list(self.list, "docs/user/", "list.html", request.user, request.META['HTTP_USER_AGENT'])
			if request.user.is_anonymous:
				self.template_name = get_template_anon_user_list(self.list, "docs/user/anon_list.html", request.user, request.META['HTTP_USER_AGENT'])
				self.is_user_can_see_doc_section = creator.is_anon_user_can_see_doc()
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


class AddDocInList(View):
	def post(self, request, *args, **kwargs):
		from common.templates import render_for_platform
		from tinytag import TinyTag

		list = DocsList.objects.get(pk=self.kwargs["pk"])
		if request.is_ajax() and list.is_user_can_create_el(request.user.pk):
			docs, order, count = [], list.count, 0
			uploaded_file = request.FILES['file']
			for file in request.FILES.getlist('file'):
				count += 1
				order += 1
				doc = Doc.objects.create(
					creator=request.user,
					file=file,
					list=list,
					title=file.name,
					order=order,
					community=list.community
				)
				docs += [doc,]
			list.count = order
			list.save(update_fields=["count"])
			if list.community:
				list.community.plus_docs(count)
			else:
				list.creator.plus_docs(count)
			return render_for_platform(request, 'docs/new_docs.html',{'object_list': docs, 'list': list, 'community': list.community})
		else:
			raise Http404


class DocRemove(View):
    def get(self, request, *args, **kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (doc.creator.pk == request.user.pk or doc.list.creator.pk == request.user.pk):
            doc.delete_doc()
            return HttpResponse()
        else:
            raise Http404
class DocRestore(View):
    def get(self,request,*args,**kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (doc.creator.pk == request.user.pk or doc.list.creator.pk == request.user.pk):
            doc.restore_doc()
            return HttpResponse()
        else:
            raise Http404

class DocEdit(TemplateView):
	form_post = None

	def get(self,request,*args,**kwargs):
		self.doc = Doc.objects.get(pk=self.kwargs["pk"])
		self.template_name = get_settings_template("docs/doc_create/edit_doc.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(DocEdit,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		from docs.forms import DocForm
		context = super(DocEdit,self).get_context_data(**kwargs)
		context["form_post"] = DocForm(instance=self.doc)
		context["doc"] = self.doc
		return context

	def post(self,request,*args,**kwargs):
		from docs.forms import DocForm
		
		doc = Doc.objects.get(pk=self.kwargs["pk"])
		form_post = DocForm(request.POST, instance=doc)

		if request.is_ajax() and form_post.is_valid():
			_doc = form_post.save(commit=False)
			doc.title = _doc.title
			doc.type_2 = _doc.type_2
			doc.save(update_fields=["title", "type_2"])
			return render_for_platform(request, 'users/docs/doc.html',{'object': doc})
		else:
			return HttpResponseBadRequest()

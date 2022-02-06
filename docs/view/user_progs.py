from docs.models import Doc, DocsList
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from docs.forms import DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.templates import get_settings_template, render_for_platform
from common.check.user import check_user_can_get_list


class UserDocCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("docs/doc_create/u_create_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDocCreate,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = DocForm(request.POST, request.FILES)

        if request.is_ajax() and form_post.is_valid():
            doc = form_post.save(commit=False)
            new_doc = doc.create_doc(creator=request.user,title=doc.title,file=doc.file,list=doc.list,community=None, type_2=doc.type_2)
            return render_for_platform(request, 'docs/doc_create/u_new_doc.html',{'doc': new_doc})
        else:
            return HttpResponseBadRequest()

class UserDocEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.doc, self.template_name = Doc.objects.get(pk=self.kwargs["doc_pk"]), get_settings_template("docs/doc_create/u_edit_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDocEdit,self).get_context_data(**kwargs)
        context["form_post"] = DocForm(instance=self.doc)
        context["doc"] = self.doc
        return context

    def post(self,request,*args,**kwargs):
        form_post = DocForm(request.POST, request.FILES)
        if request.is_ajax() and form_post.is_valid() and request.user.pk == self.doc.creator.pk:
            _doc = form_post.save(commit=False)
            new_doc = _doc.edit_doc(title=_doc.title,file=_doc.file,list=_doc.list, type_2=_doc.type_2)
            return render_for_platform(request, 'users/docs/doc.html',{'object': new_doc})
        else:
            return HttpResponseBadRequest()

class UserDocRemove(View):
    def get(self, request, *args, **kwargs):
        doc = Doc.objects.get(pk=self.kwargs["doc_pk"])
        if request.is_ajax() and request.user.pk == doc.creator.pk:
            doc.delete_item(None)
            return HttpResponse()
        else:
            raise Http404

class UserDocAbortRemove(View):
    def get(self, request, *args, **kwargs):
        doc = Doc.objects.get(pk=self.kwargs["doc_pk"])
        if request.is_ajax() and request.user.pk == doc.creator.pk:
            doc.restore_item(None)
            return HttpResponse()
        else:
            raise Http404

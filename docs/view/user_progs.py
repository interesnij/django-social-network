from docs.models import Doc, DocsList
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from docs.forms import DocslistForm, DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.templates import get_settings_template, render_for_platform
from common.check.user import check_user_can_get_list


class AddDocListInUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = DocsList.objects.get(pk=self.kwargs["list_pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_add_list(request.user.pk):
            list.add_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()

class RemoveDocListFromUserCollections(View):
    def get(self,request,*args,**kwargs):
        list = DocsList.objects.get(pk=self.kwargs["pk"])
        check_user_can_get_list(request.user, list.creator)
        if request.is_ajax() and list.is_user_can_delete_list(request.user.pk):
            list.remove_in_user_collections(request.user)
            return HttpResponse()
        else:
            return HttpResponse()


class AddDocInUserList(View):
    """
    Добавляем документ в любой список, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc.objects.get(pk=self.kwargs["pk"]), DocsList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and not list.is_item_in_list(doc.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class RemoveDocFromUserList(View):
    """
    Удаляем документ из любого списка, если он там есть
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc.objects.get(pk=self.kwargs["pk"]), DocsList.objects.get(pk=self.kwargs["list_pk"])
        if request.is_ajax() and list.is_item_in_list(doc.pk):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404


class UserDocListCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("docs/doc_create/u_create_doc_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDocListCreate,self).get_context_data(**kwargs)
        context["form"] = DocslistForm()
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        form_post = DocslistForm(request.POST)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid():
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, community=None)
            return render_for_platform(request, 'users/docs/list/my_list.html',{'list': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()

class UserDocListEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_settings_template("docs/doc_create/u_edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDocListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDocListEdit,self).get_context_data(**kwargs)
        context["list"] = DocsList.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = DocsList.objects.get(pk=self.kwargs["pk"])
        self.form = DocslistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.pk == self.list.creator.pk:
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserDocListEdit,self).get(request,*args,**kwargs)

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


class UserDocListDelete(View):
    def get(self,request,*args,**kwargs):
        list = DocsList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk and list.type != DocsList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class UserDocListRecover(View):
    def get(self,request,*args,**kwargs):
        list = DocsList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.pk == list.creator.pk:
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


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


class UserChangeDocPosition(View):
    def post(self,request,*args,**kwargs):
        import json

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                post = Doc.objects.get(pk=item['key'])
                post.order=item['value']
                post.save(update_fields=["order"])
        return HttpResponse()

class UserChangeDocListPosition(View):
    def post(self,request,*args,**kwargs):
        import json
        from users.model.list import UserDocsListPosition

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.pk == user.pk:
            for item in json.loads(request.body):
                list = UserDocsListPosition.objects.get(list=item['key'], user=user.pk)
                list.position=item['value']
                list.save(update_fields=["position"])
        return HttpResponse()

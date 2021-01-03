from docs.models import Doc2, DocList
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from docs.forms import DoclistForm, DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.template.user import get_settings_template, render_for_platform


class UserDocAdd(View):
    """
    Добавляем документ в свой список, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc2.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_doc_in_list(doc.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class UserDocRemove(View):
    """
    Удаляем документ
    """
    def get(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and list.is_doc_in_list(doc.pk):
            doc.remove()
            return HttpResponse()
        else:
            raise Http404

class UserDocListAdd(View):
    """
    Добавляем документ в любой список, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc2.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_doc_in_list(doc.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class UserDocListRemove(View):
    """
    Удаляем документ из любого списка, если он там есть
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc2.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_doc_in_list(doc.pk):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404

class UserCreateDoclistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_settings_template("docs/doc_create/u_create_doc_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCreateDoclistWindow,self).get(request,*args,**kwargs)

class UserCreateDocWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_settings_template("docs/doc_create/u_create_doc.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserCreateDocWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCreateDocWindow,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context


class UserDoclistCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserDoclistCreate,self).get_context_data(**kwargs)
        context["form_post"] = DoclistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post, user = DoclistForm(request.POST), User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid() and request.user == user:
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            if not new_list.order:
                new_list.order = 0
            new_list.save()
            return render_for_platform(request, 'users/user_docs/user_doc_list/my_list.html',{'list': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserDocCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserDocCreate,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post, user = DocForm(request.POST, request.FILES), User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user == user:
            list, new_doc = DocList.objects.get(creator_id=user.pk, community__isnull=Truee, type=DocList.MAIN), form_post.save(commit=False)
            new_doc.creator_id = request.user.pk
            lists = form_post.cleaned_data.get("list")
            new_doc.save()
            for _list in lists:
                _list.doc_list.add(new_doc)
            return render_for_platform(request, 'docs/doc_create/new_user_doc.html',{'object': new_doc})
        else:
            return HttpResponseBadRequest()


class UserDoclistEdit(TemplateView):
    """
    изменение списка документов пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user, self.template_name = User.objects.get(pk=self.kwargs["pk"]), get_settings_template("docs/doc_create/u_edit_list.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserDoclistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserDoclistEdit,self).get_context_data(**kwargs)
        context["user"] = self.user
        context["list"] = DocList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
        self.form, self.user = DoclistForm(request.POST,instance=self.list), User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(UserDoclistEdit,self).get(request,*args,**kwargs)

class UserDoclistDelete(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and self.kwargs["pk"] == request.user.pk and list.type == DocList.LIST:
            list.is_deleted = True
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class UserDoclistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and self.kwargs["pk"] == request.user.pk:
            list.is_deleted = False
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404


class UserDoclistPreview(TemplateView):
	template_name, paginate_by = None, 15

	def get(self,request,*args,**kwargs):
		self.list, self.template_name = DocList.objects.get(pk=self.kwargs["pk"]), get_settings_template("docs/doc_create/list_preview.html", request.user, request.META['HTTP_USER_AGENT'])
		return super(UserDoclistPreview,self).get(request,*args,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(UserDoclistPreview,self).get_context_data(**kwargs)
		context["list"] = self.list
		return context

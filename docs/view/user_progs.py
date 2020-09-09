from docs.models import *
from users.models import User
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from docs.forms import DoclistForm, DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.http import Http404
from common.template.user import get_settings_template


class UserDocAdd(View):
    """
    Добавляем документ в свой список, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        list = DocList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_doc_in_list(doc.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class UserDocRemove(View):
    """
    Удаляем документ из своего списка, если он там есть
    """
    def get(self, request, *args, **kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_doc_in_list(doc.pk):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404

class UserDocListAdd(View):
    """
    Добавляем документ в любой список, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        list = DocList.objects.get(uuid=self.kwargs["uuid"])

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
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_doc_in_list(doc.pk):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404

class UserCreateDoclistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("doc_create/", "u_create_doc_list.html", request)
        return super(UserCreateDoclistWindow,self).get(request,*args,**kwargs)

class UserCreateDocWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_settings_template("doc_create/", "u_create_doc.html", request)
        return super(UserCreateDocWindow,self).get(request,*args,**kwargs)


class UserDoclistCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserDoclistCreate,self).get_context_data(**kwargs)
        context["form_post"] = DoclistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = DoclistForm(request.POST)
        user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user == user:
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            if not new_list.order:
                new_list.order = 0
            new_list.save()
            return render(request, 'user_doc_list/my_list.html',{'list': new_list, 'user': request.user})
        else:
            return HttpResponseBadRequest()


class UserDocCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(UserDocCreate,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = DocForm(request.POST, request.FILES)
        user = User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user == user:
            list = DocList.objects.get(creator_id=user.pk, community=None, type=DocList.MAIN)
            new_doc = form_post.save(commit=False)
            new_doc.creator = request.user
            lists = form_post.cleaned_data.get("list")
            new_doc.save()
            if not lists:
                list.doc_list.add(new_doc)
            else:
                for _list in lists:
                    _list.doc_list.add(new_doc)

            return render(request, 'doc_create/new_user_doc.html',{'object': new_doc})
        else:
            return HttpResponseBadRequest()

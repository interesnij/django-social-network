from docs.models import *
from communities.models import Community
from django.views import View
from django.views.generic.base import TemplateView
from rest_framework.exceptions import PermissionDenied
from docs.forms import DoclistForm, DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.http import Http404


class CommunityDocAdd(View):
    """
    Добавляем документ в список документов сообщества, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["pk"])
        list = DocList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_doc_in_list(doc.pk) and request.user.is_staff_of_community_with_name(list.community.name):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class CommunityDocRemove(View):
    """
    Удаляем документ
    """
    def get(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["doc_pk"])
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community_with_name(community.name):
            doc.remove()
            return HttpResponse()
        else:
            raise Http404

class CommunityDocListAdd(View):
    """
    Добавляем документ в любой список сообщества, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["pk"])
        list = DocList.objects.get(uuid=self.kwargs["uuid"])

        if request.is_ajax() and not list.is_doc_in_list(doc.pk) and request.user.is_staff_of_community_with_name(list.community.name):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class CommunityDocListRemove(View):
    """
    Удаляем документ из любого списка сообщества, если он там есть
    """
    def get(self, request, *args, **kwargs):
        doc = Doc2.objects.get(pk=self.kwargs["pk"])
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_doc_in_list(doc.pk) and request.user.is_staff_of_community_with_name(list.community.name):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404

class CommunityCreateDoclistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_manage_template(folder="doc_create/", template="c_create_doc_list.html", request=request)
        return super(CommunityCreateDoclistWindow,self).get(request,*args,**kwargs)

class CommunityCreateDocWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = self.community.get_manage_template(folder="doc_create/", template="c_create_doc.html", request=request)
        return super(CommunityCreateDocWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityCreateDocWindow,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        context["community"] = self.community
        return context


class CommunityDoclistCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(CommunityDoclistCreate,self).get_context_data(**kwargs)
        context["form_post"] = DoclistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = DoclistForm(request.POST)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community_with_name(community.name):
            new_list = form_post.save(commit=False)
            new_list.creator = request.user
            new_list.community = community
            if not new_list.order:
                new_list.order = 0
            new_list.save()
            return render(request, 'c_docs_list/admin_list.html',{'list': new_list, 'community': community})
        else:
            return HttpResponseBadRequest()


class CommunityDocCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(CommunityDocCreate,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = DocForm(request.POST, request.FILES)
        community = Community.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form_post.is_valid() and request.user == user:
            list = DocList.objects.get(community_id=community.pk, community=None, type=DocList.MAIN)
            new_doc = form_post.save(commit=False)
            new_doc.creator = community.creator
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

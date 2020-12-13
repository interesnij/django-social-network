from docs.models import *
from communities.models import Community
from django.views import View
from django.views.generic.base import TemplateView
from docs.forms import DoclistForm, DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.template.user import render_for_platform
from common.template.community import get_community_manage_template


class CommunityDocAdd(View):
    """
    Добавляем документ в список документов сообщества, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc2.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_doc_in_list(doc.pk) and request.user.is_staff_of_community(list.community.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class CommunityDocRemove(View):
    """
    Удаляем документ
    """
    def get(self, request, *args, **kwargs):
        doc, community = Doc2.objects.get(pk=self.kwargs["doc_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            doc.remove()
            return HttpResponse()
        else:
            raise Http404

class CommunityDocListAdd(View):
    """
    Добавляем документ в любой список сообщества, если его там нет
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc2.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_doc_in_list(doc.pk) and request.user.is_staff_of_community(list.community.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class CommunityDocListRemove(View):
    """
    Удаляем документ из любого списка сообщества, если он там есть
    """
    def get(self, request, *args, **kwargs):
        doc, list = Doc2.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_doc_in_list(doc.pk) and request.user.is_staff_of_community(list.community.pk):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404

class CommunityCreateDoclistWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("docs/doc_create/c_create_doc_list.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        return super(CommunityCreateDoclistWindow,self).get(request,*args,**kwargs)

class CommunityCreateDocWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("docs/doc_create/c_create_doc.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
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
        form_post, community = DoclistForm(request.POST), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(community.pk):
            new_list = form_post.save(commit=False)
            new_list.creator, new_list.community = request.user, community
            if not new_list.order:
                new_list.order = 0
            new_list.save()
            return render_for_platform(request, 'communities/docs_list/admin_list.html',{'list': new_list, 'community': community})
        else:
            return HttpResponseBadRequest()


class CommunityDocCreate(View):
    form_post = None

    def get_context_data(self,**kwargs):
        context = super(CommunityDocCreate,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post, community = DocForm(request.POST, request.FILES), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid() and request.user.is_administrator_of_community(community.pk):
            list = DocList.objects.get(community_id=community.pk, type=DocList.MAIN)
            new_doc = form_post.save(commit=False)
            new_doc.creator, new_doc.is_community, lists = community.creator, True, form_post.cleaned_data.get("list")
            new_doc.save()
            if not lists:
                list.doc_list.add(new_doc)
            else:
                for _list in lists:
                    _list.doc_list.add(new_doc)
            return render_for_platform(request, 'docs/doc_create/new_user_doc.html',{'object': new_doc})
        else:
            return HttpResponseBadRequest()


class CommunityDoclistEdit(TemplateView):
    """
    изменение списка документов пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_community_manage_template("docs/doc_create/c_edit_list.html", request.user, self.community.pk, request.META['HTTP_USER_AGENT'])
        return super(CommunityDoclistEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDoclistEdit,self).get_context_data(**kwargs)
        context["community"] = self.community
        context["list"] = DocList.objects.get(uuid=self.kwargs["uuid"])
        return context

    def post(self,request,*args,**kwargs):
        self.list, self.form, self.community = DocList.objects.get(uuid=self.kwargs["uuid"]), PlaylistForm(request.POST,instance=self.list), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and self.form.is_valid() and self.user == request.user:
            list = self.form.save(commit=False)
            self.form.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityDoclistEdit,self).get(request,*args,**kwargs)

class CommunityDoclistDelete(View):
    def get(self,request,*args,**kwargs):
        community, list = Community.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk) and list.type == DocList.LIST:
            list.is_deleted = True
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class CommunityDoclistAbortDelete(View):
    def get(self,request,*args,**kwargs):
        community, list = Community.objects.get(pk=self.kwargs["pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(community.pk):
            list.is_deleted = False
            list.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

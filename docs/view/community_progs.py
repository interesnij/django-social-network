from docs.models import Doc, DocList
from communities.models import Community
from django.views import View
from django.views.generic.base import TemplateView
from docs.forms import DoclistForm, DocForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from common.template.user import render_for_platform
from common.template.community import get_community_manage_template
from common.check.community import check_can_get_lists


class AddDocListInCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list, community = DocList.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_community_can_add_list(community.pk):
            list.communities.add(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class RemoveDocListFromCommunityCollections(View):
    def post(self,request,*args,**kwargs):
        list, community = DocList.objects.get(uuid=self.kwargs["uuid"]), Community.objects.get(pk=self.kwargs["pk"])
        check_can_get_lists(request.user, community)
        if request.is_ajax() and list.is_user_can_delete_list(community.pk):
            list.communities.remove(community)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class AddDocInCommunityList(View):
    def get(self, request, *args, **kwargs):
        doc, list = Doc.objects.get(pk=self.kwargs["doc_pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not list.is_item_in_list(doc.pk) and request.user.is_staff_of_community(list.community.pk):
            list.doc_list.add(doc)
            return HttpResponse()
        else:
            raise Http404

class RemoveDocFromCommunityList(View):
    def get(self, request, *args, **kwargs):
        doc, list = Doc.objects.get(pk=self.kwargs["doc_pk"]), DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and list.is_item_in_list(doc.pk) and request.user.is_staff_of_community(list.community.pk):
            list.doc_list.remove(doc)
            return HttpResponse()
        else:
            raise Http404


class CommunityDocCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_community_manage_template("docs/doc_create/c_create_doc.html", request.user, Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'])
        return super(CommunityDocCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDocCreate,self).get_context_data(**kwargs)
        context["form_post"] = DocForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post = DocForm(request.POST, request.FILES)
        if request.is_ajax() and form_post.is_valid() and request.user.is_administrator_of_community(self.kwargs["pk"]):
            doc = form_post.save(commit=False)
            new_doc = doc.create_doc(creator=request.user,title=doc.title,file=doc.file,lists=request.POST.getlist("list"),is_public=request.POST.get("is_public"),community=Community.objects.get(pk=self.kwargs["pk"]))
            return render_for_platform(request, 'docs/doc_create/c_new_doc.html',{'doc': new_doc})
        else:
            return HttpResponseBadRequest()

class CommunityDocEdit(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.doc, self.template_name = Doc.objects.get(pk=self.kwargs["doc_pk"]), get_community_manage_template("docs/doc_create/c_edit_doc.html", request.user, Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'])
        return super(CommunityDocEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDocEdit,self).get_context_data(**kwargs)
        context["form_post"] = DocForm(request.POST,instance=self.doc)
        context["doc"] = self.doc
        return context

    def post(self,request,*args,**kwargs):
        form_post, DocForm(request.POST, request.FILES)
        if request.is_ajax() and form_post.is_valid() and request.user.is_administrator_of_community(self.kwargs["pk"]):
            doc = form_post.save(commit=False)
            new_doc = doc.edit_doc(title=doc.title,file=doc.file,lists=request.POST.getlist("lists"),is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'communities/docs/doc.html',{'object': new_doc})
        else:
            return HttpResponseBadRequest()


class CommunityDocListCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_community_manage_template("docs/doc_create/c_create_doc_list.html", request.user, Community.objects.get(pk=self.kwargs["pk"]), request.META['HTTP_USER_AGENT'])
        return super(CommunityDocListCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityDocListCreate,self).get_context_data(**kwargs)
        context["form_post"] = DoclistForm()
        return context

    def post(self,request,*args,**kwargs):
        form_post, community = DoclistForm(request.POST), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and form_post.is_valid() and request.user.is_staff_of_community(community.pk):
            list = form_post.save(commit=False)
            new_list = list.create_list(creator=request.user, name=list.name, description=list.description, order=list.order, community=community,is_public=request.POST.get("is_public"))
            return render_for_platform(request, 'communities/docs/list/admin_list.html',{'list': new_list, 'community': community})
        else:
            return HttpResponseBadRequest()

class CommunityDocListEdit(TemplateView):
    """
    изменение списка документов пользователя
    """
    template_name = None

    def get(self,request,*args,**kwargs):
        self.c = Community.objects.get(pk=self.kwargs["pk"])
        self.template_name = get_community_manage_template("docs/doc_create/c_edit_list.html", request.user, self.c, request.META['HTTP_USER_AGENT'])
        return super(CommunityDocListEdit,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        c = super(CommunityDocListEdit,self).get_context_data(**kwargs)
        c["community"], c["list"] = self.c, DocList.objects.get(uuid=self.kwargs["uuid"])
        return c

    def post(self,request,*args,**kwargs):
        self.list = DocList.objects.get(uuid=self.kwargs["uuid"])
        self.form = PlaylistForm(request.POST,instance=self.list)
        if request.is_ajax() and self.form.is_valid() and request.user.is_administrator_of_community(self.kwargs["pk"]):
            list = self.form.save(commit=False)
            list.edit_list(name=list.name, description=list.description, order=list.order, is_public=request.POST.get("is_public"))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()
        return super(CommunityDocListEdit,self).get(request,*args,**kwargs)


class CommunityDocListDelete(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]) and list.type != DocList.MAIN:
            list.delete_item()
            return HttpResponse()
        else:
            raise Http404

class CommunityDocListRecover(View):
    def get(self,request,*args,**kwargs):
        list = DocList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_staff_of_community(self.kwargs["pk"]):
            list.restore_item()
            return HttpResponse()
        else:
            raise Http404


class CommunityDocRemove(View):
    def get(self, request, *args, **kwargs):
        doc, c = Doc.objects.get(pk=self.kwargs["doc_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            doc.delete_item(c)
            return HttpResponse()
        else:
            raise Http404

class CommunityDocAbortRemove(View):
    def get(self, request, *args, **kwargs):
        doc, c = Doc.objects.get(pk=self.kwargs["doc_pk"]), Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_staff_of_community(c.pk):
            doc.restore_item(c)
            return HttpResponse()
        else:
            raise Http404

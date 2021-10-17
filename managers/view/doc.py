from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from common.staff_progs.doc import *
from docs.models import Doc, DocsList
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_doc import DocManageLog


class DocAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_doc_administrator():
            add_doc_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class DocAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_doc_administrator():
            remove_doc_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class DocModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_doc_moderator():
            add_doc_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class DocModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_doc_moderator():
            remove_doc_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class DocEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_doc_editor():
            add_doc_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class DocEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_doc_editor():
            remove_doc_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class DocWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_doc_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class DocWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_doc_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class DocWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_doc_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class DocWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_doc_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class DocWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_doc_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class DocWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_doc_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class DocCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_doc_manager():
            self.template_name = get_staff_template("managers/manage_create/doc/doc_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(DocCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(DocCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Doc.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        doc, form = Doc.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_doc_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=doc.pk, type=18)
            moderate_obj.create_close(object=doc, description=mod.description, manager_id=request.user.pk)
            DocManageLog.objects.create(item=doc.pk, manager=request.user.pk, action_type=DocManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class DocCloseDelete(View):
    def get(self,request,*args,**kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_doc_manager():
            moderate_obj = Moderated.objects.get(object_id=doc.pk, type=18)
            moderate_obj.delete_close(object=doc, manager_id=request.user.pk)
            DocManageLog.objects.create(item=doc.pk, manager=request.user.pk, action_type=DocManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class DocClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.doc = Doc.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 18, self.doc.pk)
        self.template_name = get_staff_template("managers/manage_create/doc/doc_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(DocClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.forms import ReportForm

        context = super(DocClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.doc
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        doc = Doc.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 18, doc.pk):
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=18, object_id=doc.pk, description=request.POST.get('description'), type=request.POST.get('type'))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class DocRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_doc_manager():
            doc = Doc.objects.get(pk=self.kwargs["pk"])
            moderate_obj = Moderated.objects.get(object_id=doc.pk, type=18)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            DocManageLog.objects.create(item=doc.pk, manager=request.user.pk, action_type=DocManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class DocUnverify(View):
    def get(self,request,*args,**kwargs):
        doc = Doc.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=doc.pk, type=18)
        if request.is_ajax() and request.user.is_doc_manager():
            obj.unverify_moderation(doc, manager_id=request.user.pk)
            DocManageLog.objects.create(item=obj.object_id, manager=request.user.pk, action_type=DocManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class ListDocClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = DocsList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 17, self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/doc/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListDocClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListDocClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = DocsList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 17, self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=17, object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListDocRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = DocsList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_doc_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=17)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            DocManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=DocManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListDocUnverify(View):
    def get(self,request,*args,**kwargs):
        list = DocsList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=17)
        if request.is_ajax() and request.user.is_doc_manager():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            DocManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=DocManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListDocCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = DocsList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_doc_manager():
            self.template_name = get_staff_template("managers/manage_create/doc/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListDocCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListDocCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = DocsList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_doc_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=17)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            DocManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=DocManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListDocCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = DocsList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_doc_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=17)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            DocManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=DocManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

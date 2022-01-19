from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from survey.models import Survey, SurveyList
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_survey import SurveyManageLog


class SurveyCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/survey/survey_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SurveyCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SurveyCloseCreate,self).get_context_data(**kwargs)
        context["object"] = Survey.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        survey, form = Survey.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=survey.pk, type=22)
            moderate_obj.create_close(object=survey, description=mod.description, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=survey.pk, manager=request.user.pk, action_type=SurveyManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class SurveyCloseDelete(View):
    def get(self,request,*args,**kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=survey.pk, type=22)
            moderate_obj.delete_close(object=survey, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=survey.pk, manager=request.user.pk, action_type=SurveyManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class SurveyClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.survey = Survey.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 22, self.survey.pk)
        self.template_name = get_staff_template("managers/manage_create/survey/survey_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SurveyClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.forms import ReportForm

        context = super(SurveyClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.survey
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        survey = Survey.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 22, survey.pk):
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=22, object_id=survey.pk, description=request.POST.get('description'), type=request.POST.get('type'))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class SurveyRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_moderator():
            survey = Survey.objects.get(pk=self.kwargs["pk"])
            moderate_obj = Moderated.objects.get(object_id=survey.pk, type=22)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=survey.pk, manager=request.user.pk, action_type=SurveyManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class SurveyUnverify(View):
    def get(self,request,*args,**kwargs):
        survey = Survey.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=survey.pk, type=22)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(survey, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=obj.object_id, manager=request.user.pk, action_type=SurveyManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class ListSurveyClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 21, self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/survey/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListSurveyClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListSurveyClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 21, self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=21, object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListSurveyRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=21)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListSurveyUnverify(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=21)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListSurveyCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/survey/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListSurveyCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListSurveyCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=21)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListSurveyCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = SurveyList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=21)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            SurveyManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=SurveyManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

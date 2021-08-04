from django.views import View
from django.views.generic.base import TemplateView
from users.models import User
from communities.models import Community
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.community import *
from managers.models import Moderated
from managers.forms import ModeratedForm, ReportForm
from django.http import Http404
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_user_community import CommunityManageLog


class CommunityAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_administrator()):
            add_community_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_administrator()):
            remove_community_administrator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален админ пользователей')
            return HttpResponse()
        else:
            raise Http404

class CommunityModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_moderator()):
            add_community_moderator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Добавлен модератор пользователей')
            return HttpResponse()
        else:
            raise Http404

class CommunityModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_moderator()):
            remove_community_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_editor()):
            add_community_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_editor()):
            remove_community_editor(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален редактор пользователей')
            return HttpResponse()
        else:
            raise Http404


class CommunityAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_advertiser()):
            add_community_advertiser(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_community_advertiser()):
            remove_community_advertiser(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_community_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_community_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_community_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_community_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_community_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_community_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_community_advertiser_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunityWorkerAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_community_advertiser_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class CommunitySuspensionCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_community_manager():
            self.template_name = get_staff_template("managers/manage_create/community_suspend.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunitySuspensionCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunitySuspensionCreate,self).get_context_data(**kwargs)
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        from django.utils import timezone

        form = ModeratedForm(request.POST)

        if request.is_ajax() and form.is_valid() and request.user.is_community_manager():
            mod = form.save(commit=False)
            number = request.POST.get('number')
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=self.kwargs["pk"], type=2)
            moderate_obj.status = Moderated.SUSPEND
            moderate_obj.description = mod.description
            moderate_obj.type = ""
            moderate_obj.save()
            if severity_int == '4':
                duration_of_penalty = timezone.timedelta(days=30)
                CommunityManageLog.objects.create(item=self.pk, manager=request.user.pk, action_type=CommunityManageLog.SEVERITY_CRITICAL)
            elif severity_int == '3':
                duration_of_penalty = timezone.timedelta(days=7)
                CommunityManageLog.objects.create(item=self.pk, manager=request.user.pk, action_type=CommunityManageLog.SEVERITY_HIGH)
            elif severity_int == '2':
                duration_of_penalty = timezone.timedelta(days=3)
                CommunityManageLog.objects.create(item=self.pk, manager=request.user.pk, action_type=CommunityManageLog.SEVERITY_MEDIUM)
            elif severity_int == '1':
                duration_of_penalty = timezone.timedelta(hours=6)
                CommunityManageLog.objects.create(item=self.pk, manager=request.user.pk, action_type=CommunityManageLog.SEVERITY_LOW)
            moderate_obj.create_suspend(manager_id=request.user.pk, duration_of_penalty=duration_of_penalty)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunitySuspensionDelete(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_community_manager():
            moderate_obj = Moderated.objects.get(type=2, object_id=self.kwargs["pk"])
            moderate_obj.delete_suspend(manager_id=request.user.pk)
            CommunityManageLog.objects.create(item=self.kwargs["pk"], manager=request.user.pk, action_type=CommunityManageLog.SUSPENDED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class CommunityCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_community_manager():
            self.template_name = get_staff_template("managers/manage_create/community_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_community_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(type=2, object_id=community.pk)
            moderate_obj.create_close(object=community, description=mod.description, manager_id=request.user.pk)
            CommunityManageLog.objects.create(item=self.kwargs["pk"], manager=request.user.pk, action_type=CommunityManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunityCloseDelete(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_community_manager():
            moderate_obj = Moderated.objects.get(type=2, object_id=self.kwargs["pk"])
            moderate_obj.delete_close(object=community, manager_id=request.user.pk)
            CommunityManageLog.objects.create(item=self.kwargs["pk"], manager=request.user.pk, action_type=CommunityManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class CommunityWarningBannerCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community = Community.objects.get(pk=self.kwargs["pk"])
        if request.user.is_community_manager():
            self.template_name = get_staff_template("managers/manage_create/community_warning_banner.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommunityWarningBannerCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityWarningBannerCreate,self).get_context_data(**kwargs)
        context["community"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        form = ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_community_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(type=2, object_id=self.kwargs["pk"])
            moderate_obj.status = Moderated.BANNER_GET
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_warning_banner(manager_id=request.user.pk)
            CommunityManageLog.objects.create(item=self.kwargs["pk"], manager=request.user.pk, action_type=CommunityManageLog.WARNING_BANNER)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunityClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.community, self.template_name = Community.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("managers/manage_create/community_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommunityClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommunityClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.community
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        form = ReportForm(request.POST)
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 2, self.kwargs["pk"]):
            mod = form.save(commit=False)
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=2, object_id=self.kwargs["pk"], description=mod.description, type=request.POST.get('type'))
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommunityWarningBannerDelete(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_community_manager():
            moderate_obj = Moderated.objects.get(type=2, object_id=self.kwargs["pk"])
            moderate_obj.delete_warning_banner(manager_id=request.user.pk)
            CommunityManageLog.objects.create(item=self.kwargs["pk"], manager=request.user.pk, action_type=CommunityManageLog.WARNING_BANNER_HIDE)
            return HttpResponse()
        else:
            raise Http404

class CommunityRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_community_manager():
            moderate_obj = Moderated.objects.get(type=2, object_id=self.kwargs["pk"])
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            CommunityManageLog.objects.create(item=self.kwargs["pk"], manager=request.user.pk, action_type=CommunityManageLog.REJECT)
            return HttpResponse()
        else:
            raise Http404

class CommunityUnverify(View):
    def get(self,request,*args,**kwargs):
        community = Community.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=community.pk, type=2)
        if request.is_ajax() and request.user.is_community_manager():
            obj.unverify_moderation(community, manager_id=request.user.pk)
            CommunityManageLog.objects.create(item=community.pk, manager=request.user.pk, action_type=CommunityManageLog.UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

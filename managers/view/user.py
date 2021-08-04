from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.user import *
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_user_community import UserManageLog


class UserAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_administrator():
            add_user_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_administrator():
            remove_user_administrator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален админ пользователей')
            return HttpResponse()
        else:
            raise Http404

class UserModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_moderator():
            add_user_moderator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Добавлен модератор пользователей')
            return HttpResponse()
        else:
            raise Http404

class UserModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_moderator():
            remove_user_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_editor():
            add_user_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_editor():
            remove_user_editor(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален редактор пользователей')
            return HttpResponse()
        else:
            raise Http404

class UserAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_advertiser():
            add_user_advertiser(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_advertiser():
            remove_user_advertiser(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_user_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_user_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_user_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_user_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_user_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_user_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_user_advertiser_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserWorkerAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_user_advertiser_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserSuspensionCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_user_manager():
            self.template_name = get_staff_template("managers/manage_create/user/user_suspend.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserSuspensionCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSuspensionCreate,self).get_context_data(**kwargs)
        context["object"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        form, user = ModeratedForm(request.POST), User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form.is_valid() and request.user.is_user_manager():
            from django.utils import timezone

            mod = form.save(commit=False)
            number = request.POST.get('number')
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=user.pk, type=1)
            moderate_obj.status = Moderated.SUSPEND
            moderate_obj.description = mod.description
            moderate_obj.save()
            if number == '4':
                duration_of_penalty = timezone.now() + timezone.timedelta(days=30)
                UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.SEVERITY_CRITICAL)
            elif number == '3':
                duration_of_penalty = timezone.now() + timezone.timedelta(days=7)
                UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.SEVERITY_HIGH)
            elif number == '2':
                duration_of_penalty = timezone.now() + timezone.timedelta(days=3)
                UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.SEVERITY_MEDIUM)
            elif number == '1':
                duration_of_penalty = timezone.now() + timezone.timedelta(hours=6)
                UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.SEVERITY_LOW)
            moderate_obj.create_suspend(manager_id=request.user.pk, duration_of_penalty=duration_of_penalty)
            user.suspend_item()
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserSuspensionDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_user_manager():
            moderate_obj = Moderated.objects.get(object_id=user.pk, type=1)
            moderate_obj.delete_suspend(manager_id=request.user.pk)
            UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.SUSPENDED_HIDE)
            user.abort_suspend_item()
            return HttpResponse()
        else:
            raise Http404

class UserCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_user_manager():
            self.template_name = get_staff_template("managers/manage_create/user/user_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCloseCreate,self).get_context_data(**kwargs)
        context["object"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        user, form = User.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_user_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=user.pk, type=1)
            moderate_obj.create_close(object=user, description=mod.description, manager_id=request.user.pk)
            UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserCloseDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_user_manager():
            moderate_obj = Moderated.objects.get(object_id=user.pk, type=1)
            moderate_obj.delete_close(object=user, manager_id=request.user.pk)
            UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class UserWarningBannerCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_user_manager():
            self.template_name = get_detect_platform_template("managers/manage_create/user/user_warning_banner.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserWarningBannerCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserWarningBannerCreate,self).get_context_data(**kwargs)
        context["object"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def post(self,request,*args,**kwargs):
        user, form = User.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_user_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=user.pk, type=1)
            moderate_obj.status = Moderated.BANNER_GET
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_warning_banner(manager_id=request.user.pk)
            UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.WARNING_BANNER)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.user = User.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 1, self.user.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/user/user_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.user
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 1, user.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=1, object_id=user.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserWarningBannerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_user_manager():
            moderate_obj = Moderated.objects.get(object_id=user.pk, type=1)
            moderate_obj.delete_warning_banner(manager_id=request.user.pk)
            UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.WARNING_BANNER_HIDE)
            return HttpResponse()
        else:
            raise Http404

class UserRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_user_manager():
            moderate_obj = Moderated.objects.get(object_id=user.pk, type=1)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.REJECT)
            return HttpResponse()
        else:
            raise Http404

class UserUnverify(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["user_pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=user.pk, type=1)
        if request.is_ajax() and request.user.is_user_manager():
            obj.unverify_moderation(user, manager_id=request.user.pk)
            UserManageLog.objects.create(user=user.pk, manager=request.user.pk, action_type=UserManageLog.UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

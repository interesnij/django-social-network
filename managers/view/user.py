from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.user import *
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.template.user import get_detect_platform_template


class UserAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_administrator()):
            add_user_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_administrator()):
            remove_user_administrator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален админ пользователей')
            return HttpResponse()
        else:
            raise Http404

class UserModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_moderator()):
            add_user_moderator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Добавлен модератор пользователей')
            return HttpResponse()
        else:
            raise Http404

class UserModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_moderator()):
            remove_user_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_editor()):
            add_user_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_editor()):
            remove_user_editor(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален редактор пользователей')
            return HttpResponse()
        else:
            raise Http404

class UserAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_advertiser()):
            add_user_advertiser(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class UserAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_advertiser()):
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

class UserSuspensionCreate(View):
    def post(self,request,*args,**kwargs):
        form, user = UserModeratedForm(request.POST), User.objects.get(pk=self.kwargs["pk"])

        if request.is_ajax() and form.is_valid() and (request.user.is_user_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            number = request.POST.get('number')
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=user.pk, type="USE")
            moderate_obj.status = Moderated.SUSPEND
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_suspend(manager_id=request.user.pk, severity_int=number)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserSuspensionDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_user_manager() or request.user.is_superuser:
            moderate_obj = Moderated.objects.get(object_id=user.pk, type="USE")
            moderate_obj.delete_suspend(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class UserCloseCreate(View):
    def post(self,request,*args,**kwargs):
        user, form = User.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_user_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=user.pk, type="USE")
            moderate_obj.create_close(object=user, description=mod.description, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserCloseDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_user_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=user.pk, type="USE")
            moderate_obj.delete_close(object=user, manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class UserWarningBannerCreate(View):
    def post(self,request,*args,**kwargs):
        user, form = User.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_user_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=user.pk, type="USE")
            moderate_obj.status = Moderated.BANNER_GET
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_warning_banner(manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class UserClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        user = User.objects.get(pk=self.kwargs["pk"])
        form = ReportForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_authenticated:
            mod = form.save(commit=False)
            ModerationReport.create_user_moderation_report(reporter_id=request.user.pk, object_id=user.pk, _type="USE", description=mod.description, type=request.POST.get('type'))
            return HttpResponse()
        else:
            raise Http404

class UserWarningBannerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_user_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=user.pk, type="USE")
            moderate_obj.delete_warning_banner(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class UserRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_user_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=user.pk, type="USE")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class UserSuspendWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_user_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/user_suspend.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserSuspendWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSuspendWindow,self).get_context_data(**kwargs)
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context

class UserCloseWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_user_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/user_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserCloseWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserCloseWindow,self).get_context_data(**kwargs)
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context

class UserWarningBannerdWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_user_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/user_warning_banner.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(UserWarningBannerdWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserWarningBannerdWindow,self).get_context_data(**kwargs)
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context

class UserClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/user_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(UserClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserClaimWindow,self).get_context_data(**kwargs)
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context


class UserUnverify(View):
    def get(self,request,*args,**kwargs):
        user, obj = User.objects.get(pk=self.kwargs["user_pk"]), Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_user_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

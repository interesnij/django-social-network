from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.user import *
from managers.forms import UserModeratedForm
from django.views.generic.base import TemplateView
from managers.model.user import ModeratedUser


class UserAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_administrator:
            add_user_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_administrator:
            remove_user_administrator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален админ пользователей')
        return HttpResponse("")


class UserModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_moderator:
            add_user_moderator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Добавлен модератор пользователей')
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_moderator:
            remove_user_moderator(user, request.user)
        return HttpResponse("")


class UserEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_editor:
            add_user_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_editor:
            remove_user_editor(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален редактор пользователей')
        return HttpResponse("")


class UserAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_advertiser:
            add_user_advertiser(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_advertiser:
            remove_user_advertiser(user, request.user)
        return HttpResponse("")


class UserWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_administrator_worker(user, request.user)
        return HttpResponse("")


class UserWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_moderator_worker(user, request.user)
        return HttpResponse("")


class UserWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_editor_worker(user, request.user)
        return HttpResponse("")


class UserWorkerAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_advertiser_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_advertiser_worker(user, request.user)
        return HttpResponse("")


class UserSuspensionCreate(View):
    def post(self,request,*args,**kwargs):
        form = UserModeratedForm(request.POST)
        user = User.objects.get(pk=self.kwargs["pk"])

        if form.is_valid() and (request.user.is_user_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            number = request.POST.get('number')
            moderate_obj = ModeratedUser.get_or_create_moderated_object_for_user(user)
            moderate_obj.status = ModeratedUser.STATUS_SUSPEND
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_suspend(manager_id=request.user.pk, user_id=user.pk, severity_int=number)
            return HttpResponse("ok")
        else:
            return HttpResponse("bad request")

class UserSuspensionDelete(View):
    def get(self,request,*args,**kwargs):
        moderate_obj = ModeratedUser.objects.get(pk=self.kwargs["pk"])
        if request.user.is_user_manager or request.user.is_superuser:
            moderate_obj.delete_suspend(manager_id=request.user.pk, user_id=moderate_obj.user.pk)
        return HttpResponse("")

class UserBlockCreate(View):
    def get(self,request,*args,**kwargs):
        moderate_obj = ModeratedUser.objects.get(pk=self.kwargs["pk"])
        severity_int = self.kwargs["number"]
        if request.user.is_user_manager or request.user.is_superuser:
            moderate_obj.create_block(manager_id=request.user.pk, user_id=moderate_obj.user.pk)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserBlockDelete(View):
    def get(self,request,*args,**kwargs):
        moderate_obj = ModeratedUser.objects.get(pk=self.kwargs["pk"])
        if request.user.is_user_manager or request.user.is_superuser:
            moderate_obj.delete_block(manager_id=request.user.pk, user_id=moderate_obj.user.pk)
        return HttpResponse("")

class UserWarningBannerCreate(View):
    def get(self,request,*args,**kwargs):
        moderate_obj = ModeratedUser.objects.get(pk=self.kwargs["pk"])
        severity_int = self.kwargs["number"]
        if request.user.is_user_manager or request.user.is_superuser:
            moderate_obj.create_warning_banner(manager_id=request.user.pk, user_id=moderate_obj.user.pk)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWarningBannerDelete(View):
    def get(self,request,*args,**kwargs):
        moderate_obj = ModeratedUser.objects.get(pk=self.kwargs["pk"])
        if request.user.is_user_manager or request.user.is_superuser:
            moderate_obj.delete_warning_banner(manager_id=request.user.pk, user_id=moderate_obj.user.pk)
        return HttpResponse("")

class UserRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        moderate_obj = ModeratedUser.objects.get(pk=self.kwargs["pk"])
        severity_int = self.kwargs["number"]
        if request.user.is_user_manager or request.user.is_superuser:
            moderate_obj.reject_moderation(manager_id=request.user.pk, user_id=moderate_obj.user.pk)
            return HttpResponse("")
        else:
            return HttpResponse("")


class UserSuspendWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_user_manager or request.user.is_superuser:
            self.template_name = "manage_create/create_user_suspend.html"
        else:
            self.template_name = "about.html"
        return super(UserSuspendWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserSuspendWindow,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

class UserBlockWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_user_manager or request.user.is_superuser:
            self.template_name = "manage_create/create_user_block.html"
        else:
            self.template_name = "about.html"
        return super(UserBlockWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserBlockWindow,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

class UserWarningBannerdWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_user_manager or request.user.is_superuser:
            self.template_name = "manage_create/create_user_warning_banner.html"
        else:
            self.template_name = "about.html"
        return super(UserWarningBannerdWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(UserWarningBannerdWindow,self).get_context_data(**kwargs)
        context["user"] = self.user
        return context

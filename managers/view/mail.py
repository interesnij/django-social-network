from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.mail import *
from mail.models import Mail
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_mail import MailManageLog


class MailAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_mail_administrator():
            add_mail_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_mail_administrator():
            remove_mail_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_mail_moderator():
            add_mail_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_mail_moderator():
            remove_mail_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_mail_editor():
            add_mail_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_mail_editor():
            remove_mail_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_mail_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_mail_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_mail_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_mail_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_mail_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_mail_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MailCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Mail.objects.get(pk=self.kwargs["pk"])
        if request.user.is_mail_manager():
            self.template_name = get_staff_template("managers/manage_create/mail/mail_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(MailCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(MailCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Mail.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_mail_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=54)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            MailManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MailManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class MailCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Mail.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_mail_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=54)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            MailManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MailManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class MailClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/mail/mail_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Mail.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 54, self.new.pk)
        return super(MailClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(MailClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Mail.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 54, self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=54, object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class MailRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Mail.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_mail_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=54)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            MailManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MailManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class MailUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Mail.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=54)
        if request.is_ajax() and request.user.is_mail_manager():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            MailManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MailManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

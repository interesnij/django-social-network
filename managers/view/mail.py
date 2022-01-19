from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from mail.models import Mail
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_mail import MailManageLog


class MailCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Mail.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator():
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
        if request.is_ajax() and form.is_valid() and request.user.is_administrator():
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
        if request.is_ajax() and request.user.is_administrator():
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
        if request.is_ajax() and request.user.is_administrator():
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
        if request.is_ajax() and request.user.is_administrator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            MailManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MailManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.message import *
from message.models import Message
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_message import MessageManageLog


class MessageAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_message_administrator():
            add_message_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_message_administrator():
            remove_message_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_message_moderator():
            add_message_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_message_moderator():
            remove_message_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_message_editor():
            add_message_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_message_editor():
            remove_message_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_message_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_message_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_message_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_message_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_message_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_message_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class MessageCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Message.objects.get(pk=self.kwargs["pk"])
        if request.user.is_message_manager():
            self.template_name = get_staff_template("managers/manage_create/message/message_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(MessageCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(MessageCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Message.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_message_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=55)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            MessageManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MessageManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class MessageCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Message.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_message_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=55)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            MessageManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MessageManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class MessageClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/message/message_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Message.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 55, self.new.pk)
        return super(MessageClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(MessageClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Message.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 55, self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=55, object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class MessageRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Message.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_message_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=55)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            MessageManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MessageManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class MailUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Message.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=55)
        if request.is_ajax() and request.user.is_message_manager():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            MessageManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MessageManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from chat.models import Message
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_message import MessageManageLog


class MessageCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Message.objects.get(pk=self.kwargs["pk"])
        if request.user.is_administrator():
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
        if request.is_ajax() and form.is_valid() and request.user.is_administrator():
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
        if request.is_ajax() and request.user.is_administrator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=55)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            MessageManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MessageManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class MessageRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Message.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
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
        if request.is_ajax() and request.user.is_administrator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            MessageManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=MessageManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class SendManagerMessages(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_administrator():
            self.template_name = get_detect_platform_template("managers/manage_create/message/send_messages.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SendManagerMessages,self).get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        if request.is_ajax() and form.is_valid() and request.user.is_administrator():
            from chat.models import Chat
            from chat.forms import MessageForm

            form = MessageForm(request.POST, request.FILES)
            form_post = form.save(commit=False)
            Chat.get_or_create_manager_chat_and_send_message(
                creator_pk = request.user.pk,
                text = form_post.text,
                voice = request.POST.get('voice'),
                attach = request.POST.getlist('attach_items')
            )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

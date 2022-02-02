from django.views.generic.base import TemplateView
from common.templates import get_detect_platform_template
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views import View
from users.models import User


class ManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ManagersView,self).get(request,*args,**kwargs)

class SuperManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SuperManagersView,self).get(request,*args,**kwargs)


class SendManagerMessages(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_administrator():
            self.template_name = get_detect_platform_template("managers/manage_create/message/send_messages.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SendManagerMessages,self).get(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        from chat.forms import MessageForm

        form = MessageForm(request.POST, request.FILES)

        if request.is_ajax() and form.is_valid() and request.user.is_administrator():
            from chat.models import Chat

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

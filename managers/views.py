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


class UserAdministratorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser():
            user.perm = 10
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserAdministratorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 9
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()


class UserHighManagerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 8
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserHighManagerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserManagerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 7
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserManagerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserTraineeManagerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 6
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserTraineeManagerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()


class UserTraineeSupportCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 4
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserTraineeSupportDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserSupportCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 5
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserSupportDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()


class UserTraineeModeratorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 2
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserTraineeModeratorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserModeratorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 3
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserModeratorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()


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

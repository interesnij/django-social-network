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
            from chat.models import Message

            form_post = form.save(commit=False)
            Message.get_or_create_manager_chat_and_send_message(
                creator_pk = request.user.pk,
                text = form_post.text,
                voice = request.POST.get('voice'),
                attach = request.POST.getlist('attach_items')
            )
            return HttpResponse()
        else:
            return HttpResponseBadRequest()


class SanctionCreate(TemplateView):
    template_name, open_suspend, open_warning_banner, is_admin = None, None, None, None

    def get(self,request,*args,**kwargs):
        from common.utils import get_item_of_type, get_comment, get_list_of_type

        self._type = request.GET.get('type')
        self._subtype = request.GET.get('subtype')

        if self._subtype and self._subtype == "comment":
            self.item = get_comment(self._type)
        elif _subtype and _subtype == "planner":
            self.item = get_planner(self._type)
        elif _type[0] == "l":
            self.item = get_list_of_type(self._type)
            open_suspend = True
        elif "use" in self._type:
            from users.models import User
            self.item = User.objects.get(pk=self._type[3:])
            open_suspend, open_warning_banner, is_admin = True, True, True
        elif "com" in self._type:
            from communities.models import Community
            self.item = Community.objects.get(pk=self._type[3:])
            open_suspend, open_warning_banner, is_admin = True, True, True
        else:
            self.item = get_item_of_type(self._type)

        if (is_admin and request.user.is_administrator()) or request.user.is_moderator():
            self.template_name = get_detect_platform_template("generic/sanction.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SanctionCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SanctionCreate,self).get_context_data(**kwargs)
        context["object"] = self.item
        context["type"] = self._type
        context["subtype"] = self._subtype
        context["open_suspend"] = self.open_suspend
        context["open_warning_banner"] = self.open_warning_banner
        return context

    def post(self, request, *args, **kwargs):
        from django.http import HttpResponse, HttpResponseBadRequest
        from managers.models import Moderated, ModerationReport
        from common.utils import get_item_for_post_sanction

        list = get_item_for_post_sanction(request.POST.get('_type'), request.POST.get('_subtype'))
        if not (list[4] and request.user.is_administrator()) or not request.user.is_moderator():
            return HttpResponseBadRequest()
        if request.is_ajax():
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=t, object_id=item.pk, description=post.description, type=post.type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

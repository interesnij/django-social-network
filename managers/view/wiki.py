from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from wiki.models import Wiki
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_wiki import WikiManageLog


class WikiCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.wiki = Wiki.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/wiki/wiki_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(WikiCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(WikiCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.wiki
        return context

    def post(self,request,*args,**kwargs):
        wiki, form = Wiki.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=wiki.pk, type=56)
            moderate_obj.create_close(object=wiki, description=mod.description, manager_id=request.user.pk)
            WikiManageLog.objects.create(item=wiki.pk, manager=request.user.pk, action_type=WikiManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class WikiCloseDelete(View):
    def get(self,request,*args,**kwargs):
        wiki = Wiki.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=wiki.pk, type=56)
            moderate_obj.delete_close(object=wiki, manager_id=request.user.pk)
            WikiManageLog.objects.create(item=wiki.pk, manager=request.user.pk, action_type=WikiManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class WikiClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/wiki/wiki_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.wiki = Wiki.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 56, self.wiki.pk)
        return super(WikiClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(WikiClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.wiki
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.wiki = Wiki.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 56, self.wiki.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=56, object_id=self.wiki.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class WikiRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        wiki = Wiki.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=wiki.pk, type=56)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            WikiManageLog.objects.create(item=wiki.pk, manager=request.user.pk, action_type=WikiManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class WikiUnverify(View):
    def get(self,request,*args,**kwargs):
        wiki = Wiki.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=wiki.pk, type=56)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            WikiManageLog.objects.create(item=wiki.pk, manager=request.user.pk, action_type=WikiManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

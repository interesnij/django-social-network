from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from site.models import Site
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_site import SiteManageLog


class SiteCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Site.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/site/site_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(SiteCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(SiteCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Site.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=6)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            SiteManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=SiteManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class SiteCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Site.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=6)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            SiteManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=SiteManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class SiteClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/site/site_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Site.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 6, self.new.pk)
        return super(SiteClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(SiteClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Site.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 6, self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=6, object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class SiteRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Site.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=6)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            SiteManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=SiteManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class SiteUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Site.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=6)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            SiteManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=SiteManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

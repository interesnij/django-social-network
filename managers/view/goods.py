from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.goods import *
from goods.models import Good, GoodComment
from managers.forms import ModeratedForm, ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.template.user import get_detect_platform_template


class GoodAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_good_administrator()):
            add_good_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser and request.user.is_work_good_administrator()):
            remove_good_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_good_moderator()):
            add_good_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_good_moderator()):
            remove_good_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_good_editor()):
            add_good_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_good_editor():
            remove_good_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_good_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_good_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_good_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_good_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_good_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_good_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodCloseCreate(View):
    def post(self,request,*args,**kwargs):
        good, form = Good.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_good_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=good.pk, type="GOO")
            moderate_obj.create_close(object=good, description=mod.description, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class GoodCloseDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=self.kwargs["pk"], type="GOO")
            moderate_obj.delete_close(object=good, manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class GoodClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="GOO", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class GoodRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=self.kwargs["pk"], type="GOO")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class GoodUnverify(View):
    def get(self,request,*args,**kwargs):
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentGoodUnverify(View):
    def get(self,request,*args,**kwargs):
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentGoodCloseCreate(View):
    def post(self,request,*args,**kwargs):
        comment, form = GoodComment.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_good_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=self.kwargs["pk"], type="GOOC")
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=self.kwargs["pk"], type="GOOC")
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax() and request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="GOOC", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(type="GOOC", object_id=self.kwargs["pk"])
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class GoodCloseWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_good_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/good/good_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GoodCloseWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCloseWindow,self).get_context_data(**kwargs)
        context["object"] = self.good
        return context

class GoodClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.photo, self.template_name = Good.objects.get(uuid=self.kwargs["uuid"]), get_detect_platform_template("managers/manage_create/good/good_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(GoodClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodClaimWindow,self).get_context_data(**kwargs)
        context["object"] = self.good
        return context


class GoodCommentCloseWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_good_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/good/good_comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GoodCommentCloseWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommentCloseWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        return context

class GoodCommentClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment, self.template_name = GoodComment.objects.get(pk=self.kwargs["pk"]), get_detect_platform_template("managers/manage_create/good/good_comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        if self.comment.parent:
            self.photo = self.comment.parent.photo
        else:
            self.photo = self.comment.photo
        return super(GoodCommentClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommentClaimWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["good"] = self.good
        return context

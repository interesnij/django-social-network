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

class GoodDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        good, form = Good.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_good_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=good.pk, type="GOO")
            moderate_obj.status = Moderated.DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk)
            good.status = "CLO"
            good.save(update_fields=['status'])
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class GoodDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=self.kwargs["pk"], type="GOO")
            moderate_obj.delete_deleted(manager_id=request.user.pk)
            good.status = "PUB"
            good.save(update_fields=['status'])
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

class CommentGoodDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        comment, form = GoodComment.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_good_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=self.kwargs["pk"], type="GOOC")
            moderate_obj.status = Moderated.DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk)
            comment.status = "CLO"
            comment.save(update_fields=['status'])
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_good_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=self.kwargs["pk"], type="GOOC")
            moderate_obj.delete_deleted(manager_id=request.user.pk)
            comment.status = "PUB"
            comment.save(update_fields=['status'])
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

class GoodDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_good_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/good/good_delete.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GoodDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodDeleteWindow,self).get_context_data(**kwargs)
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


class GoodCommentDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_good_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/good/good_comment_delete.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GoodCommentDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommentDeleteWindow,self).get_context_data(**kwargs)
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

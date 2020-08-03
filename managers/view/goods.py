from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.goods import *
from goods.models import Good, GoodComment
from managers.forms import GoodModeratedForm, GoodCommentModeratedForm
from django.views.generic.base import TemplateView
from managers.model.good import ModeratedGood, ModeratedGoodComment
from django.http import Http404


class GoodAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser or request.user.is_work_good_administrator:
            add_good_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser and request.user.is_work_good_administrator:
            remove_good_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser and request.user.is_work_good_moderator:
            add_good_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser and request.user.is_work_good_moderator:
            remove_good_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser and request.user.is_work_good_editor:
            add_good_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class GoodEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_good_editor:
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
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        form = GoodModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_good_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedGood.get_or_create_moderated_object_for_good(good)
            moderate_obj.status = ModeratedGood.STATUS_DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk, good_id=good.pk)
            good.is_deleted = True
            good.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class GoodDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_good_manager or request.user.is_superuser:
            moderate_obj = ModeratedGood.objects.get(good=good)
            moderate_obj.delete_deleted(manager_id=request.user.pk, good_id=good.pk)
            good.is_deleted = False
            good.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            raise Http404

class GoodClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.good import GoodModerationReport

        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            GoodModerationReport.create_good_moderation_report(reporter_id=request.user.pk, good=good, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class GoodRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_good_manager or request.user.is_superuser:
            moderate_obj = ModeratedGood.objects.get(good=good)
            moderate_obj.reject_moderation(manager_id=request.user.pk, good_id=good.pk)
            return HttpResponse()
        else:
            raise Http404

class GoodUnverify(View):
    def get(self,request,*args,**kwargs):
        good = Good.objects.get(uuid=self.kwargs["good_uuid"])
        obj = ModeratedGood.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and request.user.is_good_manager or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk, good_id=good.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentGoodUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        obj = ModeratedGoodComment.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and request.user.is_good_manager or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk, comment_id=comment.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentGoodDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        form = GoodCommentModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_good_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedGoodComment.get_or_create_moderated_object_for_comment(comment)
            moderate_obj.status = ModeratedGoodComment.STATUS_DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk, comment_id=comment.pk)
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_good_manager or request.user.is_superuser:
            moderate_obj = ModeratedGoodComment.objects.get(comment=comment)
            moderate_obj.delete_deleted(manager_id=request.user.pk, comment_id=comment.pk)
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.good import GoodCommentModerationReport

        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            GoodCommentModerationReport.create_good_comment_moderation_report(reporter_id=request.user.pk, comment=comment, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_good_manager or request.user.is_superuser:
            moderate_obj = ModeratedGoodComment.objects.get(comment=comment)
            moderate_obj.reject_moderation(manager_id=request.user.pk, comment_id=comment.pk)
            return HttpResponse()
        else:
            raise Http404

class GoodDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.good = Good.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_good_manager or request.user.is_superuser:
            self.template_name = "manage_create/good/good_delete.html"
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
        self.photo = Good.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = "manage_create/good/good_claim.html"
        return super(GoodClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodClaimWindow,self).get_context_data(**kwargs)
        context["object"] = self.good
        return context


class GoodCommentDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_good_manager or request.user.is_superuser:
            self.template_name = "manage_create/good/good_comment_delete.html"
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
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        try:
            self.photo = self.comment.parent_comment.photo
        except:
            self.photo = self.comment.photo
        self.template_name = "manage_create/good/good_comment_claim.html"
        return super(GoodCommentClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCommentClaimWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["good"] = self.good
        return context

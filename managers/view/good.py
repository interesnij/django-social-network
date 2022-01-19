from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from goods.models import GoodList, Good, GoodComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_good import GoodManageLog


class GoodCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Good.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/good/good_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(GoodCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(GoodCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Good.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=34)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=GoodManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class GoodCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=34)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=GoodManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class GoodClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/good/good_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Good.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 34, self.new.pk)
        return super(GoodClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(GoodClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 34, self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=34, object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class GoodRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Good.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=34)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            GoodManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=GoodManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class GoodUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Good.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=34)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=GoodManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class CommentGoodClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 35, self.comment.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/good/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentGoodClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentGoodClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 35, comment.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=35, object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=35)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            GoodManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=GoodManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentGoodUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=35)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=GoodManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentGoodCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/good/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentGoodCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentGoodCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=35)
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=GoodManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentGoodCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = GoodComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=35)
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=GoodManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class ListGoodClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 33, self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/good/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListGoodClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListGoodClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 33, self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=33, object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListGoodRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=33)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            GoodManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=GoodManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListGoodUnverify(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=33)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=GoodManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListGoodCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/good/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListGoodCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListGoodCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=33)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=GoodManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListGoodCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = GoodList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=33)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            GoodManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=GoodManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

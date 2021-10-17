from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.post import *
from posts.models import PostsList, Post, PostComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_post import PostManageLog


class PostAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_post_administrator():
            add_post_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_post_administrator():
            remove_post_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_post_moderator():
            add_post_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_post_moderator():
            remove_post_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_post_editor():
            add_post_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_work_post_editor():
            remove_post_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_post_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_post_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_post_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_post_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_post_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_post_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(pk=self.kwargs["pk"])
        if request.user.is_post_manager():
            self.template_name = get_staff_template("managers/manage_create/post/post_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PostCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Post.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_post_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=9)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            PostManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PostManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PostCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_post_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=9)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            PostManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PostManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class PostClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/post/post_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Post.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 9, self.new.pk)
        return super(PostClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(PostClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 9, self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=9, object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_post_manager():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=9)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PostManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PostManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class PostUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=9)
        if request.is_ajax() and request.user.is_post_manager():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            PostManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PostManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class CommentPostClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 10, self.comment.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/post/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentPostClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentPostClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 10, comment.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=10, object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_post_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=10)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PostManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PostManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentPostUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=10)
        if request.is_ajax() and request.user.is_post_manager():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            PostManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PostManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentPostCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_post_manager():
            self.template_name = get_staff_template("managers/manage_create/post/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentPostCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentPostCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_post_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=10)
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            PostManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PostManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPostCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_post_manager():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=10)
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            PostManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PostManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class ListPostClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = PostsList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 8, self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/post/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListPostClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListPostClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = PostsList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 8, self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=8, object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListPostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_post_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=8)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PostManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PostManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListPostUnverify(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=8)
        if request.is_ajax() and request.user.is_post_manager():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            PostManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PostManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListPostCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = PostsList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager():
            self.template_name = get_staff_template("managers/manage_create/post/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListPostCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListPostCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = PostsList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_post_manager():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=8)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            PostManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PostManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListPostCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_post_manager():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=8)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            PostManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PostManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

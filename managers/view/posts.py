from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.posts import *
from posts.models import Post, PostComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.template.user import get_detect_platform_template


class PostAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_post_administrator()):
            add_post_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_post_administrator()):
            remove_post_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_post_moderator()):
            add_post_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_post_moderator()):
            remove_post_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_post_editor()):
            add_post_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_post_editor()):
            remove_post_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PostWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_post_administrator_worker(user, request.user)
            return HttpResponse("")
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

class PostDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        post, form = Post.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_post_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type="POS")
            moderate_obj.status = Moderated.DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk)
            post.status = "CLO"
            post.save(update_fields=['status'])
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PostDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and (request.user.is_post_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="POS")
            moderate_obj.delete_deleted(manager_id=request.user.pk)
            post.status = "PRI"
            post.save(update_fields=['status'])
            return HttpResponse()
        else:
            raise Http404

class PostClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="POS", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and (request.user.is_post_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=post.pk, type="POS")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404


class PostUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["post_uuid"])
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_post_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentPostUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_post_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentPostDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and (request.user.is_post_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedPostComment.get_or_create_moderated_object(object_id=comment.pk, type="POSC")
            moderate_obj.status = Moderated.DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk)
            comment.status = "CLO"
            comment.save(update_fields=['status'])
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPostDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_post_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="POSC")
            moderate_obj.delete_deleted(manager_id=request.user.pk)
            comment.status = "PUB"
            comment.save(update_fields=['status'])
            return HttpResponse()
        else:
            raise Http404

class CommentPostClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="POSС", object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_post_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="POSC")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class PostDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/post/post_delete.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PostDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostDeleteWindow,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

class PostClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/post/post_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostClaimWindow,self).get_context_data(**kwargs)
        context["object"] = Post.objects.get(uuid=self.kwargs["uuid"])
        return context


class PostCommentDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_post_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/post/post_comment_delete.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PostCommentDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommentDeleteWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        return context

class PostCommentClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        try:
            self.post = self.comment.parent.post
        except:
            self.post = self.comment.post
        self.template_name = get_detect_platform_template("managers/manage_create/post/post_comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(PostCommentClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommentClaimWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["post"] = self.post
        return context

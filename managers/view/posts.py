from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.posts import *
from posts.models import Post, PostComment
from managers.forms import PostModeratedForm, PostCommentModeratedForm
from django.views.generic.base import TemplateView
from managers.model.post import ModeratedPost, ModeratedPostComment


class PostAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_post_administrator:
            add_post_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_administrator:
            remove_post_administrator(user, request.user)
        return HttpResponse("")


class PostModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_moderator:
            add_post_moderator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_moderator:
            remove_post_moderator(user, request.user)
        return HttpResponse("")


class PostEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_editor:
            add_post_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_editor:
            remove_post_editor(user, request.user)
        return HttpResponse("")


class PostWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_post_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_post_administrator_worker(user, request.user)
        return HttpResponse("")


class PostWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_post_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_post_moderator_worker(user, request.user)
        return HttpResponse("")


class PostWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_post_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_post_editor_worker(user, request.user)
        return HttpResponse("")


class PostDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        form = PostModeratedForm(request.POST)
        if form.is_valid() and (request.user.is_post_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedPost.get_or_create_moderated_object_for_post(post)
            moderate_obj.status = ModeratedPost.STATUS_DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk, post_id=post.pk)
            post.is_deleted = True
            post.save(update_fields=['is_deleted'])
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            moderate_obj = ModeratedPost.objects.get(post=post)
            moderate_obj.delete_deleted(manager_id=request.user.pk, post_id=post.pk)
            post.is_deleted = False
            post.save(update_fields=['is_deleted'])
        return HttpResponse("")


class PostClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.post import PostModerationReport

        post = Post.objects.get(uuid=self.kwargs["uuid"])
        description = request.POST.get('description')
        type = request.POST.get('type')
        PostModerationReport.create_post_moderation_report(reporter_id=request.user.pk, post=post, description=description, type=type)
        return HttpResponse("!")

class PostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            moderate_obj = ModeratedPost.objects.get(post=post)
            moderate_obj.reject_moderation(manager_id=request.user.pk, post_id=post.pk)
            return HttpResponse("")
        else:
            return HttpResponse("")


class PostUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["post_uuid"])
        obj = ModeratedPost.objects.get(pk=self.kwargs["obj_pk"])
        obj.unverify_moderation(manager_id=request.user.pk, post_id=post.pk)
        return HttpResponse("")


class CommentPostUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        obj = ModeratedPostComment.objects.get(pk=self.kwargs["obj_pk"])
        obj.unverify_moderation(manager_id=request.user.pk, comment_id=comment.pk)
        return HttpResponse("")

class CommentPostDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        form = PostCommentModeratedForm(request.POST)
        if form.is_valid() and (request.user.is_post_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedPostComment.get_or_create_moderated_object_for_comment(comment)
            moderate_obj.status = ModeratedPostComment.STATUS_DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk, comment_id=comment.pk)
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommentPostDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_post_manager or request.user.is_superuser:
            moderate_obj = ModeratedPostComment.objects.get(comment=comment)
            moderate_obj.delete_deleted(manager_id=request.user.pk, comment_id=comment.pk)
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class CommentPostClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.post import PostCommentModerationReport

        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        description = request.POST.get('description')
        type = request.POST.get('type')
        PostCommentModerationReport.create_post_comment_moderation_report(reporter_id=request.user.pk, comment=comment, description=description, type=type)
        return HttpResponse("!")

class CommentPostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_post_manager or request.user.is_superuser:
            moderate_obj = ModeratedPostComment.objects.get(comment=comment)
            moderate_obj.reject_moderation(manager_id=request.user.pk, comment_id=comment.pk)
            return HttpResponse("")
        else:
            return HttpResponse("")


class PostDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            self.template_name = "manage_create/post/post_delete.html"
        else:
            self.template_name = "about.html"
        return super(PostDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostDeleteWindow,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

class PostClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            self.template_name = "manage_create/post/post_claim.html"
        else:
            self.template_name = "about.html"
        return super(PostClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostClaimWindow,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context


class PostCommentDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_post_manager or request.user.is_superuser:
            self.template_name = "manage_create/post/post_comment_delete.html"
        else:
            self.template_name = "about.html"
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
            self.post = self.comment.parent_comment.post
        except:
            self.post = self.comment.post
        if request.user.is_post_manager or request.user.is_superuser:
            self.template_name = "manage_create/post/post_comment_claim.html"
        else:
            self.template_name = "about.html"
        return super(PostCommentClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostCommentClaimWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["post"] = self.post
        return context

from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.posts import *
from posts.models import Post
from managers.forms import PostModeratedForm, PostReportForm
from django.views.generic.base import TemplateView
from managers.model.post import ModeratedPost


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


class PostSuspensionCreate(View):
    def post(self,request,*args,**kwargs):
        form = PostModeratedForm(request.POST)
        post = Post.objects.get(uuid=self.kwargs["uuid"])

        if form.is_valid() and (request.user.is_post_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            number = request.POST.get('number')
            moderate_obj = ModeratedPost.get_or_create_moderated_object_for_post(post)
            moderate_obj.status = ModeratedPost.STATUS_SUSPEND
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_suspend(manager_id=request.user.pk, post_id=post.pk, severity_int=number)
            return HttpResponse("ok")
        else:
            return HttpResponse("bad request")

class PostSuspensionDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            moderate_obj = ModeratedPost.objects.get(post=post)
            moderate_obj.delete_suspend(manager_id=request.user.pk, post_id=post.pk)
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
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            moderate_obj = ModeratedPost.objects.get(post=post)
            moderate_obj.delete_deleted(manager_id=request.user.pk, post_id=post.pk)
        return HttpResponse("")


class PostClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.post import PostModerationReport

        post = Post.objects.get(uuid=self.kwargs["uuid"])
        form = PostReportForm(request.POST)
        if request.user.is_authenticated:
            mod = form.save(commit=False)
            if not mod.description:
                description = "Без описания"
            else:
                description = mod.description
            PostModerationReport.create_post_moderation_report(reporter_id=request.user.pk, post=post, description=description, type=request.POST.get('type'))
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            moderate_obj = ModeratedPost.objects.get(post=post)
            moderate_obj.reject_moderation(manager_id=request.user.pk, post_id=post.pk)
            return HttpResponse("")
        else:
            return HttpResponse("")


class PostSuspendWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            self.template_name = "manage_create/post_suspend.html"
        else:
            self.template_name = "about.html"
        return super(PostSuspendWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostSuspendWindow,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

class PostDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_post_manager or request.user.is_superuser:
            self.template_name = "manage_create/post_delete.html"
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
            self.template_name = "manage_create/post_claim.html"
        else:
            self.template_name = "about.html"
        return super(PostClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PostClaimWindow,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context


class PostUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(uuid=self.kwargs["post_uuid"])
        obj = ModeratedPost.objects.get(pk=self.kwargs["obj_pk"])
        obj.unverify_moderation(manager_id=request.user.pk, post_id=post.pk)
        return HttpResponse("")

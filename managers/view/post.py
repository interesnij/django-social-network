from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from posts.models import PostsList, Post, PostComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_post import PostManageLog


class PostCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Post.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
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
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
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
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=9)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            PostManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PostManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class PostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Post.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
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
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            PostManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PostManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class CommentPostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
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
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            PostManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PostManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentPostCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PostComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
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
        if form.is_valid() and request.user.is_moderator():
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
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=10)
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            PostManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PostManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class ListPostRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = PostsList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
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
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            PostManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PostManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListPostCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = PostsList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_moderator():
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
        if form.is_valid() and request.user.is_moderator():
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
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=8)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            PostManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PostManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

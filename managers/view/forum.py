from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from forum.models import Forum, ForumComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_forum import ForumManageLog


class ForumCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Forum.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/forum/forum_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ForumCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ForumCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Forum.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=45)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            ForumManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ForumManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ForumCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Forum.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=45)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            ForumManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ForumManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class ForumRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Forum.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=45)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ForumManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ForumManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ForumUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Forum.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=45)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            ForumManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=ForumManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class CommentForumRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = ForumComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=46)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            ForumManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ForumManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentForumUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = ForumComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=46)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            ForumManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ForumManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentForumCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = ForumComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/forum/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentForumCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentForumCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = ForumComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=46)
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            ForumManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ForumManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentForumCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = ForumComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=46)
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            ForumManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=ForumManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

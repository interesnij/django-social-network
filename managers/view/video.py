from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from video.models import VideoList, Video, VideoComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_video import VideoManageLog


class VideoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Video.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/video/video_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(VideoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Video.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=30)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=VideoManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class VideoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=30)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=VideoManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class VideoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/video/video_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Video.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 13, self.new.pk)
        return super(VideoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(VideoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 30, self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=30, object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class VideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Video.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=30)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            VideoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=VideoManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class VideoUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Video.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=30)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=VideoManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class CommentVideoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 31, self.comment.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/video/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentVideoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentVideoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 31, comment.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=31, object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentVideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=31)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            VideoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=VideoManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentVideoUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=31)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=VideoManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentVideoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/video/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentVideoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentVideoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=31)
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=VideoManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentVideoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=31)
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=VideoManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class ListVideoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 12, self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/video/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListVideoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListVideoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 29, self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=29, object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListVideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=29)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListVideoUnverify(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=29)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListVideoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/video/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListVideoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListVideoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=29)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListVideoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = VideoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=29)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            VideoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=VideoManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

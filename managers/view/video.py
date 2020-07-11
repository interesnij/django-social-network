from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.video import *
from video.models import Video, VideoComment
from managers.forms import VideoModeratedForm, VideoCommentModeratedForm
from django.views.generic.base import TemplateView
from managers.model.video import ModeratedVideo, ModeratedVideoComment


class VideoAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_video_administrator:
            add_video_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class VideoAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_video_administrator:
            remove_video_administrator(user, request.user)
        return HttpResponse("")


class VideoModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_video_moderator:
            add_video_moderator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class VideoModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_video_moderator:
            remove_video_moderator(user, request.user)
        return HttpResponse("")


class VideoEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_video_editor:
            add_video_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class VideoEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_video_editor:
            remove_video_editor(user, request.user)
        return HttpResponse("")


class VideoWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_video_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class VideoWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_video_administrator_worker(user, request.user)
        return HttpResponse("")


class VideoWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_video_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class VideoWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_video_moderator_worker(user, request.user)
        return HttpResponse("")


class VideoWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_video_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class VideoWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_video_editor_worker(user, request.user)
        return HttpResponse("")


class VideoDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        form = GoodModeratedForm(request.POST)
        if form.is_valid() and (request.user.is_video_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedVideo.get_or_create_moderated_object_for_video(video)
            moderate_obj.status = ModeratedVideo.STATUS_DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk, video_id=video.pk)
            video.is_deleted = True
            video.save(update_fields=['is_deleted'])
        return HttpResponse("")

class VideoDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_video_manager or request.user.is_superuser:
            moderate_obj = ModeratedVideo.objects.get(video=video)
            moderate_obj.delete_deleted(manager_id=request.user.pk, video_id=video.pk)
            video.is_deleted = False
            video.save(update_fields=['is_deleted'])
        return HttpResponse("")


class VideoClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.video import VideoModerationReport

        video = Video.objects.get(uuid=self.kwargs["uuid"])
        description = request.POST.get('description')
        type = request.POST.get('type')
        VideoModerationReport.create_video_moderation_report(reporter_id=request.user.pk, video=video, description=description, type=type)
        return HttpResponse("!")

class VideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_video_manager or request.user.is_superuser:
            moderate_obj = ModeratedVideo.objects.get(video=video)
            moderate_obj.reject_moderation(manager_id=request.user.pk, video_id=video.pk)
        return HttpResponse("")


class VideoUnverify(View):
    def get(self,request,*args,**kwargs):
        video = Video.objects.get(uuid=self.kwargs["video_uuid"])
        obj = ModeratedVideo.objects.get(pk=self.kwargs["obj_pk"])
        if request.user.is_video_manager or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk, video_id=video.pk)
        return HttpResponse("")


class CommentVideoUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        obj = ModeratedVideoComment.objects.get(pk=self.kwargs["obj_pk"])
        if request.user.is_video_manager or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk, comment_id=comment.pk)
        return HttpResponse("")

class CommentVideoDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        form = VideoCommentModeratedForm(request.POST)
        if form.is_valid() and (request.user.is_video_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedVideoComment.get_or_create_moderated_object_for_comment(comment)
            moderate_obj.status = ModeratedVideoComment.STATUS_DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk, comment_id=comment.pk)
            comment.is_deleted = True
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")

class CommentVideoDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_video_manager or request.user.is_superuser:
            moderate_obj = ModeratedVideoComment.objects.get(comment=comment)
            moderate_obj.delete_deleted(manager_id=request.user.pk, comment_id=comment.pk)
            comment.is_deleted = False
            comment.save(update_fields=['is_deleted'])
        return HttpResponse("")


class CommentVideoClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.video import VideoCommentModerationReport

        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        description = request.POST.get('description')
        type = request.POST.get('type')
        VideoCommentModerationReport.create_video_comment_moderation_report(reporter_id=request.user.pk, comment=comment, description=description, type=type)
        return HttpResponse("!")

class CommentVideoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_video_manager or request.user.is_superuser:
            moderate_obj = ModeratedVideoComment.objects.get(comment=comment)
            moderate_obj.reject_moderation(manager_id=request.user.pk, comment_id=comment.pk)
        return HttpResponse("")


class VideoDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_video_manager or request.user.is_superuser:
            self.template_name = "manage_create/video/video_delete.html"
        else:
            self.template_name = "about.html"
        return super(VideoDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoDeleteWindow,self).get_context_data(**kwargs)
        context["object"] = self.video
        return context

class VideoClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.video = Video.objects.get(uuid=self.kwargs["uuid"])
        self.template_name = "manage_create/video/video_claim.html"
        return super(VideoClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoClaimWindow,self).get_context_data(**kwargs)
        context["object"] = self.video
        return context


class VideoCommentDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_video_manager or request.user.is_superuser:
            self.template_name = "manage_create/video/video_comment_delete.html"
        else:
            self.template_name = "about.html"
        return super(VideoCommentDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCommentDeleteWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        return context

class VideoCommentClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = VideoComment.objects.get(pk=self.kwargs["pk"])
        try:
            self.photo = self.comment.parent_comment.photo
        except:
            self.photo = self.comment.photo
        self.template_name = "manage_create/video/video_comment_claim.html"
        return super(VideoCommentClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(VideoCommentClaimWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["video"] = self.video
        return context

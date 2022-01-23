from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from gallery.models import PhotoList, Photo, PhotoComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from common.templates import get_detect_platform_template, get_staff_template
from logs.model.manage_photo import PhotoManageLog


class PhotoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.post = Photo.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/photo/photo_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PhotoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.post
        return context

    def post(self,request,*args,**kwargs):
        post, form = Photo.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=13)
            moderate_obj.create_close(object=post, description=mod.description, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        post = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=13)
            moderate_obj.delete_close(object=post, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

class PhotoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        self.new = Photo.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 13, self.new.pk)
        return super(PhotoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        from managers.models import ModerationReport

        context = super(PhotoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.new
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.new = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 13, self.new.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=13, object_id=self.new.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        post = Photo.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=post.pk, type=13)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_REJECT)
            return HttpResponse()
        else:
            raise Http404


class PhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        post = Photo.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=post.pk, type=13)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(post, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=post.pk, manager=request.user.pk, action_type=PhotoManageLog.ITEM_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404


class CommentPhotoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 14, self.comment.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/photo/comment_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(CommentPhotoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentPhotoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 14, comment.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=14, object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=14)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PhotoManageLog.COMMENT_REJECT)
            return HttpResponse()
        else:
            raise Http404


class CommentPhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=14)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(comment, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PhotoManageLog.COMMENT_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class CommentPhotoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/photo/comment_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(CommentPhotoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(CommentPhotoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.comment
        return context

    def post(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type=14)
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PhotoManageLog.COMMENT_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPhotoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type=14)
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=comment.pk, manager=request.user.pk, action_type=PhotoManageLog.COMMENT_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404


class ListPhotoClaimCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        self.is_reported = ModerationReport.is_user_already_reported(request.user.pk, 12, self.list.pk)
        self.template_name = get_detect_platform_template("managers/manage_create/photos/list_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ListPhotoClaimCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListPhotoClaimCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        context["is_reported"] = self.is_reported
        return context

    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and not ModerationReport.is_user_already_reported(request.user.pk, 12, self.list.pk):
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type=12, object_id=self.list.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListPhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=12)
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_REJECT)
            return HttpResponse()
        else:
            raise Http404


class ListPhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=12)
        if request.is_ajax() and request.user.is_moderator():
            obj.unverify_moderation(list, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_UNVERIFY)
            return HttpResponse()
        else:
            raise Http404

class ListPhotoCloseCreate(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.user.is_moderator():
            self.template_name = get_staff_template("managers/manage_create/photos/list_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(ListPhotoCloseCreate,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(ListPhotoCloseCreate,self).get_context_data(**kwargs)
        context["object"] = self.list
        return context

    def post(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        form = ModeratedForm(request.POST)
        if form.is_valid() and request.user.is_moderator():
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=list.pk, type=12)
            moderate_obj.create_close(object=list, description=mod.description, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_CLOSED)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class ListPhotoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        list = PhotoList.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_moderator():
            moderate_obj = Moderated.objects.get(object_id=list.pk, type=12)
            moderate_obj.delete_close(object=list, manager_id=request.user.pk)
            PhotoManageLog.objects.create(item=list.pk, manager=request.user.pk, action_type=PhotoManageLog.LIST_CLOSED_HIDE)
            return HttpResponse()
        else:
            raise Http404

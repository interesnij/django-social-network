from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.photo import *
from gallery.models import Photo, PhotoComment
from managers.forms import ModeratedForm
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.template.user import get_detect_platform_template


class PhotoAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_administrator()):
            add_photo_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_administrator()):
            remove_photo_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_moderator()):
            add_photo_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_moderator()):
            remove_photo_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_editor()):
            add_photo_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_photo_editor()):
            remove_photo_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_photo_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_photo_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_photo_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_photo_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_photo_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_photo_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class PhotoCloseCreate(View):
    def post(self,request,*args,**kwargs):
        photo, form = Photo.objects.get(uuid=self.kwargs["uuid"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_photo_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=photo.pk, type="PHO")
            moderate_obj.create_close(object=photo, description=mod.description, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            moderate_obj = Moderated.objects.get(object_id=photo.pk, type="PHO")
            moderate_obj.delete_close(object=photo, manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class PhotoClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="PHO", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class PhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["uuid"])
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            moderate_obj = Moderated.objects.get(object_id=photo.pk, type="PHO")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class PhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        photo = Photo.objects.get(uuid=self.kwargs["photo_uuid"])
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentPhotoUnverify(View):
    def get(self,request,*args,**kwargs):
        comment, obj = PhotoComment.objects.get(pk=self.kwargs["pk"]), Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentPhotoCloseCreate(View):
    def post(self,request,*args,**kwargs):
        comment, form = PhotoComment.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_photo_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=comment.pk, type="PHOC")
            moderate_obj.create_close(object=comment, description=mod.description, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPhotoCloseDelete(View):
    def get(self,request,*args,**kwargs):
        comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_photo_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=comment.pk, type="PHOC")
            moderate_obj.delete_close(object=comment, manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class CommentPhotoClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax() and request.is_ajax():
            description, type = request.POST.get('description'), request.POST.get('type')
            comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
            Moderation.create_moderation_report(reporter_id=request.user.pk, _type="PHOС", object_id=comment.pk, description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class CommentPhotoRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and request.user.is_photo_manager() or request.user.is_superuser:
            moderate_obj = Moderated.objects.get(object_id=self.kwargs["pk"], type="PHOC")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404

class PhotoCloseWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_photo_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_close", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PhotoCloseWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCloseWindow,self).get_context_data(**kwargs)
        context["object"] = Photo.objects.get(uuid=self.kwargs["uuid"])
        return context

class PhotoClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_claim", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoClaimWindow,self).get_context_data(**kwargs)
        context["object"] = Photo.objects.get(uuid=self.kwargs["uuid"])
        return context


class PhotoCommentCloseWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_photo_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_comment_close", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
        return super(PhotoCommentCloseWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCommentCloseWindow,self).get_context_data(**kwargs)
        context["comment"] = PhotoComment.objects.get(pk=self.kwargs["pk"])
        return context

class PhotoCommentClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.comment = PhotoComment.objects.get(pk=self.kwargs["pk"])
        try:
            self.photo = self.comment.parent.photo
        except:
            self.photo = self.comment.photo
        self.template_name = get_detect_platform_template("managers/manage_create/photo/photo_comment_claim", request.user, request.META['HTTP_USER_AGENT'])
        return super(PhotoCommentClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(PhotoCommentClaimWindow,self).get_context_data(**kwargs)
        context["comment"] = self.comment
        context["photo"] = self.photo
        return context

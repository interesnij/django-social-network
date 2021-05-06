from django.views import View
from users.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from common.staff_progs.audio import *
from music.models import Music
from django.views.generic.base import TemplateView
from managers.models import Moderated
from django.http import Http404
from common.template.user import get_detect_platform_template


class AudioAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_audio_administrator()):
            add_audio_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class AudioAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_audio_administrator()):
            remove_audio_administrator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class AudioModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_audio_moderator()):
            add_audio_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class AudioModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_audio_moderator()):
            remove_audio_moderator(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class AudioEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_audio_editor()):
            add_audio_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class AudioEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_superuser or request.user.is_work_audio_editor()):
            remove_audio_editor(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class AudioWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_audio_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class AudioWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_audio_administrator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class AudioWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_audio_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class AudioWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_audio_moderator_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class AudioWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            add_audio_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404

class AudioWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser:
            remove_audio_editor_worker(user, request.user)
            return HttpResponse()
        else:
            raise Http404


class AudioCloseCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.forms import ModeratedForm

        audio, form = Music.objects.get(pk=self.kwargs["pk"]), ModeratedForm(request.POST)
        if request.is_ajax() and form.is_valid() and (request.user.is_audio_manager() or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = Moderated.get_or_create_moderated_object(object_id=audio.pk, type="MUS")
            moderate_obj.create_close(object=audio, description=mod.description, manager_id=request.user.pk)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class AudioCloseDelete(View):
    def get(self,request,*args,**kwargs):
        audio = Music.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and (request.user.is_audio_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=audio.pk, type="MUS")
            moderate_obj.delete_close(object=audio, manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404


class AudioClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.models import ModerationReport

        if request.is_ajax():
            description = request.POST.get('description')
            type = request.POST.get('type')
            ModerationReport.create_moderation_report(reporter_id=request.user.pk, _type="MUS", object_id=self.kwargs["pk"], description=description, type=type)
            return HttpResponse()
        else:
            return HttpResponseBadRequest()

class AudioRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        if request.is_ajax() and (request.user.is_audio_manager() or request.user.is_superuser):
            moderate_obj = Moderated.objects.get(object_id=self.kwargs["pk"], type="MUS")
            moderate_obj.reject_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404


class AudioUnverify(View):
    def get(self,request,*args,**kwargs):
        obj = Moderated.objects.get(pk=self.kwargs["obj_pk"])
        if request.is_ajax() and (request.user.is_audio_manager() or request.user.is_superuser):
            obj.unverify_moderation(manager_id=request.user.pk)
            return HttpResponse()
        else:
            raise Http404


class AudioCloseWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.is_ajax() and (request.user.is_audio_manager() or request.user.is_superuser):
            self.template_name = get_detect_platform_template("managers/manage_create/audio/audio_close.html", request.user, request.META['HTTP_USER_AGENT'])
        else:
            raise Http404
    def get_context_data(self,**kwargs):
        context = super(AudioCloseWindow,self).get_context_data(**kwargs)
        context["object"] = Music.objects.get(pk=self.kwargs["pk"])
        return context

class AudioClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.template_name = get_detect_platform_template("managers/manage_create/audio/audio_claim.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(AudioClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AudioClaimWindow,self).get_context_data(**kwargs)
        context["object"] = Music.objects.get(pk=self.kwargs["pk"])
        return context

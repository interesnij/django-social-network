from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.audio import *
from music.models import SoundcloudParsing
from managers.forms import AudioModeratedForm
from django.views.generic.base import TemplateView
from managers.model.audio import ModeratedAudio


class AudioAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_audio_administrator:
            add_audio_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class AudioAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_audio_administrator:
            remove_audio_administrator(user, request.user)
        return HttpResponse("")


class AudioModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_audio_moderator:
            add_audio_moderator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class AudioModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_audio_moderator:
            remove_audio_moderator(user, request.user)
        return HttpResponse("")


class AudioEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_audio_editor:
            add_audio_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class AudioEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_audio_editor:
            remove_audio_editor(user, request.user)
        return HttpResponse("")


class AudioWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_audio_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class AudioWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_audio_administrator_worker(user, request.user)
        return HttpResponse("")


class AudioWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_audio_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class AudioWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_audio_moderator_worker(user, request.user)
        return HttpResponse("")


class AudioWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_audio_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class AudioWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_audio_editor_worker(user, request.user)
        return HttpResponse("")


class AudioDeleteCreate(View):
    def post(self,request,*args,**kwargs):
        audio = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        form = AudioModeratedForm(request.POST)
        if form.is_valid() and (request.user.is_audio_manager or request.user.is_superuser):
            mod = form.save(commit=False)
            moderate_obj = ModeratedAudio.get_or_create_moderated_object_for_audio(audio)
            moderate_obj.status = ModeratedAudio.STATUS_DELETED
            moderate_obj.description = mod.description
            moderate_obj.save()
            moderate_obj.create_deleted(manager_id=request.user.pk, audio_id=audio.pk)
            audio.is_deleted = True
            audio.save(update_fields=['is_deleted'])
        return HttpResponse("")

class AudioDeleteDelete(View):
    def get(self,request,*args,**kwargs):
        audio = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        if request.user.is_audio_manager or request.user.is_superuser:
            moderate_obj = ModeratedAudio.objects.get(audio=audio)
            moderate_obj.delete_deleted(manager_id=request.user.pk, audio_id=audio.pk)
            audio.is_deleted = False
            audio.save(update_fields=['is_deleted'])
        return HttpResponse("")


class AudioClaimCreate(View):
    def post(self,request,*args,**kwargs):
        from managers.model.audio import AudioModerationReport

        audio = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        description = request.POST.get('description')
        type = request.POST.get('type')
        AudioModerationReport.create_audio_moderation_report(reporter_id=request.user.pk, audio=audio, description=description, type=type)
        return HttpResponse("!")

class AudioRejectedCreate(View):
    def get(self,request,*args,**kwargs):
        audio = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        if request.user.is_audio_manager or request.user.is_superuser:
            moderate_obj = ModeratedAudio.objects.get(audio=audio)
            moderate_obj.reject_moderation(manager_id=request.user.pk, audio_id=audio.pk)
        return HttpResponse("")


class AudioUnverify(View):
    def get(self,request,*args,**kwargs):
        audio = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        obj = ModeratedAudio.objects.get(pk=self.kwargs["obj_pk"])
        if request.user.is_audio_manager or request.user.is_superuser:
            obj.unverify_moderation(manager_id=request.user.pk, audio_id=audio.pk)
        return HttpResponse("")


class AudioDeleteWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.audio = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        if request.user.is_audio_manager or request.user.is_superuser:
            self.template_name = "manage_create/audio/audio_delete.html"
        else:
            self.template_name = "about.html"
        return super(AudioDeleteWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AudioDeleteWindow,self).get_context_data(**kwargs)
        context["object"] = self.audio
        return context

class AudioClaimWindow(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.audio = SoundcloudParsing.objects.get(pk=self.kwargs["pk"])
        self.template_name = "manage_create/audio/audio_claim.html"
        return super(AudioClaimWindow,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context = super(AudioClaimWindow,self).get_context_data(**kwargs)
        context["object"] = self.audio
        return context

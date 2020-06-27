from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.audio import *


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

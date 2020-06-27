from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.video import *


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

from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.photo import *


class PhotoAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_photo_administrator:
            add_photo_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PhotoAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_photo_administrator:
            remove_photo_administrator(user, request.user)
        return HttpResponse("")


class PhotoModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_photo_moderator:
            add_photo_moderator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PhotoModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_photo_moderator:
            remove_photo_moderator(user, request.user)
        return HttpResponse("")


class PhotoEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_photo_editor:
            add_photo_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PhotoEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_photo_editor:
            remove_photo_editor(user, request.user)
        return HttpResponse("")


class PhotoWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_photo_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PhotoWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_photo_administrator_worker(user, request.user)
        return HttpResponse("")


class PhotoWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_photo_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PhotoWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_photo_moderator_worker(user, request.user)
        return HttpResponse("")


class PhotoWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_photo_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PhotoWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_photo_editor_worker(user, request.user)
        return HttpResponse("")

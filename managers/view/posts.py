from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.posts import *


class PostAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_post_administrator:
            add_post_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_administrator:
            remove_post_administrator(user, request.user)
        return HttpResponse("")


class PostModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_moderator:
            add_post_moderator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_moderator:
            remove_post_moderator(user, request.user)
        return HttpResponse("")


class PostEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_editor:
            add_post_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_post_editor:
            remove_post_editor(user, request.user)
        return HttpResponse("")


class PostWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_post_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_post_administrator_worker(user, request.user)
        return HttpResponse("")


class PostWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_post_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_post_moderator_worker(user, request.user)
        return HttpResponse("")


class PostWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_post_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class PostWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_post_editor_worker(user, request.user)
        return HttpResponse("")

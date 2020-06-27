from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.goods import *


class GoodAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_good_administrator:
            add_good_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class GoodAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_good_administrator:
            remove_good_administrator(user, request.user)
        return HttpResponse("")


class GoodModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_good_moderator:
            add_good_moderator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class GoodModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_good_moderator:
            remove_good_moderator(user, request.user)
        return HttpResponse("")


class GoodEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_good_editor:
            add_good_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class GoodEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_good_editor:
            remove_good_editor(user, request.user)
        return HttpResponse("")


class GoodWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_good_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class GoodWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_good_administrator_worker(user, request.user)
        return HttpResponse("")


class GoodWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_good_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class GoodWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_good_moderator_worker(user, request.user)
        return HttpResponse("")


class GoodWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_good_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class GoodWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_good_editor_worker(user, request.user)
        return HttpResponse("")

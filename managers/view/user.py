from django.views import View
from users.models import User
from django.http import HttpResponse
from logs.models import UserWorkerLog, UserManageCreatorLog
from common.staff_progs.user import *


class UserAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_administrator:
            add_user_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_administrator:
            remove_user_administrator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален админ пользователей')
        return HttpResponse("")


class UserModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_moderator:
            add_user_moderator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Добавлен модератор пользователей')
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_moderator:
            remove_user_moderator(user, request.user)
        return HttpResponse("")


class UserEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_editor:
            add_user_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_editor:
            remove_user_editor(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален редактор пользователей')
        return HttpResponse("")


class UserAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_advertiser:
            add_user_advertiser(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_advertiser:
            remove_user_advertiser(user, request.user)
        return HttpResponse("")


class UserWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_administrator_worker(user, request.user)
        return HttpResponse("")


class UserWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_moderator_worker(user, request.user)
        return HttpResponse("")


class UserWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_editor_worker(user, request.user)
        return HttpResponse("")


class UserWorkerAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_user_advertiser_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class UserWorkerAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_user_advertiser_worker(user, request.user)
        return HttpResponse("")

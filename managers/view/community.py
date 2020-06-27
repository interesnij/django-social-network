from django.views import View
from users.models import User
from django.http import HttpResponse
from common.staff_progs.community import *


class CommunityAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser or request.user.is_work_community_administrator:
            add_community_administrator(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_community_administrator:
            remove_community_administrator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален админ пользователей')
        return HttpResponse("")


class CommunityModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_community_moderator:
            add_community_moderator(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Добавлен модератор пользователей')
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_community_moderator:
            remove_community_moderator(user, request.user)
        return HttpResponse("")


class CommunityEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_community_editor:
            add_community_editor(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_community_editor:
            remove_community_editor(user, request.user)
            UserWorkerLog.objects.create(manager=request.user, user=user, action_type='Удален редактор пользователей')
        return HttpResponse("")


class CommunityAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_community_advertiser:
            add_community_advertiser(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser and request.user.is_work_community_advertiser:
            remove_community_advertiser(user, request.user)
        return HttpResponse("")


class CommunityWorkerAdminCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_community_administrator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityWorkerAdminDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_community_administrator_worker(user, request.user)
        return HttpResponse("")


class CommunityWorkerModerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_community_moderator_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityWorkerModerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_community_moderator_worker(user, request.user)
        return HttpResponse("")


class CommunityWorkerEditorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_community_editor_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityWorkerEditorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_community_editor_worker(user, request.user)
        return HttpResponse("")


class CommunityWorkerAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            add_community_advertiser_worker(user, request.user)
            return HttpResponse("")
        else:
            return HttpResponse("")

class CommunityWorkerAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_superuser:
            remove_community_advertiser_worker(user, request.user)
        return HttpResponse("")

from django.http import HttpResponse
from django.views import View
from users.models import User


class UserAdministratorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser():
            user.perm = 10
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserAdministratorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_superuser():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserAdvertiserCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 9
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserAdvertiserDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()


class UserHighManagerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 8
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserHighManagerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserManagerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 7
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserManagerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserTraineeManagerCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 6
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserTraineeManagerDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_administrator():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()


class UserTraineeSupportCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 4
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserTraineeSupportDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserSupportCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 5
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserSupportDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()


class UserTraineeModeratorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 2
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserTraineeModeratorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

class UserModeratorCreate(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 3
            user.save(update_fields=["perm"])
        return HttpResponse()

class UserModeratorDelete(View):
    def get(self,request,*args,**kwargs):
        user = User.objects.get(pk=self.kwargs["pk"])
        if request.is_ajax() and request.user.is_manager():
            user.perm = 1
            user.save(update_fields=["perm"])
            return HttpResponse()

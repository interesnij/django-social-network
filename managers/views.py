from django.views.generic.base import TemplateView
from users.models import User
from common.template.user import get_detect_platform_template


class MainManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            self.template_name = get_detect_platform_template("managers/managers.html", request_user, request.META['HTTP_USER_AGENT'])
        return super(MainManagersView,self).get(request,*args,**kwargs)

class ManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if self.user.is_manager():
            self.template_name = get_detect_platform_template("managers/managers.html", request_user, request.META['HTTP_USER_AGENT'])
        return super(ManagersView,self).get(request,*args,**kwargs)

class SuperManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        self.user = User.objects.get(pk=self.kwargs["pk"])
        if request.user.is_supermanager():
            self.template_name = get_detect_platform_template("managers/managers.html", request_user, request.META['HTTP_USER_AGENT'])
        return super(SuperManagersView,self).get(request,*args,**kwargs)

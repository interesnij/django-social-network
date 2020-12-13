from django.views.generic.base import TemplateView
from common.template.user import get_detect_platform_template


class ManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_manager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(ManagersView,self).get(request,*args,**kwargs)

class SuperManagersView(TemplateView):
    template_name = None

    def get(self,request,*args,**kwargs):
        if request.user.is_supermanager() or request.user.is_superuser:
            self.template_name = get_detect_platform_template("managers/managers.html", request.user, request.META['HTTP_USER_AGENT'])
        return super(SuperManagersView,self).get(request,*args,**kwargs)

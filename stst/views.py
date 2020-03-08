from django.views.generic.base import TemplateView
from common.utils import get_client_ip, get_location


class StatView(TemplateView):
    template_name="stat.html"

    def get(self,request,*args,**kwargs):
        self.ip = get_client_ip(request)
        get_location(request)
        return super(StatView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(StatView,self).get_context_data(**kwargs)
        context["ip"]=self.ip
        return context

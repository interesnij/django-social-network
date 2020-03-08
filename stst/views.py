from django.views.generic.base import TemplateView
from users.model.profile import *
from common.utils import get_client_ip
import json


class StatView(TemplateView):
    template_name="stat.html"

    def get(self,request,*args,**kwargs):
        self.ip = get_client_ip(request)
        self.response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + ip)
        self.data = self.response.json()

        return super(StatView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(StatView,self).get_context_data(**kwargs)
        context["ip"]=self.ip
        context["data"]=self.data
        return context

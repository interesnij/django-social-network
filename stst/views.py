import json, requests
from django.views.generic.base import TemplateView
from users.model.profile import *
from common.utils import get_client_ip


class StatView(TemplateView):
    template_name="stat.html"

    def get(self,request,*args,**kwargs):
        self.ip = get_client_ip(request)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.olds_ip = IPUser.objects.get(user=self.user)
        except:
            self.olds_ip = IPUser.objects.create(user=self.user)

        if olds_ip.ip_3 and self.olds_ip.ip_1 != self.ip:
            self.response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + self.ip)
            self.data = self.response.json()
            loc = OneUserLocation.objects.get(user=self.user)
            loc.sity_ru = self.data.sity.name_ru
            loc.sity_en = self.data.sity.name_en
            loc.region_ru = self.data.region.name_ru
            loc.region_en = self.data.region.name_en
            loc.country_ru = self.data.sity.country_ru
            loc.country_en = self.data.sity.country_en

        return super(StatView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(StatView,self).get_context_data(**kwargs)
        context["ip"]=self.ip
        context["data"]=self.data
        return context

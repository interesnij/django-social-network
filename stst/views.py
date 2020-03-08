import json, requests
from django.views.generic.base import TemplateView
from users.model.profile import *
from common.utils import get_client_ip
from common.location import data
from users.models import User

class StatView(TemplateView):
    template_name="stat.html"

    def get(self,request,*args,**kwargs):
        self.ip = get_client_ip(request)
        self.user = User.objects.get(pk=self.kwargs["pk"])
        try:
            self.olds_ip = IPUser.objects.get(user=self.user)
        except:
            self.olds_ip = IPUser.objects.create(user=self.user)

        if not self.olds_ip.ip_1:
            #self.data = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + self.ip)
            self.data = data
            try:
                self.loc = OneUserLocation.objects.get(user=self.user)
            except:
                self.loc = OneUserLocation.objects.create(user=self.user)
            self.sity = self.data['city']
            self.region = self.data['region']
            self.country = self.data['country']
            self.loc.city_ru = self.sity['city_ru']
            self.loc.city_en = self.sity.['city_en']
            self.loc.region_ru = self.region.['region_ru']
            self.loc.region_en = self.region.['region_en']
            self.loc.country_ru = self.country.['country_ru']
            self.loc.country_en = self.country.['country_en']
            self.loc.save()
        elif not self.olds_ip.ip_2 and self.olds_ip.ip_3 != self.ip and self.olds_ip.ip_2 != self.ip and self.olds_ip.ip_1 != self.ip:
            self.response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + self.ip)
            self.data = self.response.json()
            try:
                self.loc = TwoUserLocation.objects.get(user=self.user)
            except:
                self.loc = TwoUserLocation.objects.create(user=self.user)
            self.loc.city_ru = self.data.city.name_ru
            self.loc.city_en = self.data.city.name_en
            self.loc.region_ru = self.data.region.name_ru
            self.loc.region_en = self.data.region.name_en
            self.loc.country_ru = self.data.city.country_ru
            self.loc.country_en = self.data.city.country_en
            self.loc.save()
        elif not self.olds_ip.ip_3 and self.olds_ip.ip_3 != self.ip and self.olds_ip.ip_2 != self.ip and self.olds_ip.ip_1 != self.ip:
            self.response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + self.ip)
            self.data = self.response.json()
            try:
                self.loc = ThreeUserLocation.objects.get(user=self.user)
            except:
                self.loc = ThreeUserLocation.objects.create(user=self.user)
            self.loc.city_ru = self.data.city.name_ru
            self.loc.city_en = self.data.sity.name_en
            self.loc.region_ru = self.data.region.name_ru
            self.loc.region_en = self.data.region.name_en
            self.loc.country_ru = self.data.sity.country_ru
            self.loc.country_en = self.data.sity.country_en
            self.loc.save()
        elif self.olds_ip.ip_3 and self.olds_ip.ip_3 != self.ip and self.olds_ip.ip_2 != self.ip and self.olds_ip.ip_1 != self.ip:
            self.response = requests.get(url= "http://api.sypexgeo.net/8Dbm8/json/" + self.ip)
            self.data = self.response.json()
            try:
                self.loc = ThreeUserLocation.objects.get(user=self.user)
            except:
                self.loc = ThreeUserLocation.objects.create(user=self.user)
            self.loc.ip_1 = self.ip
            self.loc.ip_2 = None
            self.loc.ip_3 = None
            self.loc.sity_ru = self.data.sity.name_ru
            self.loc.sity_en = self.data.sity.name_en
            self.loc.region_ru = self.data.region.name_ru
            self.loc.region_en = self.data.region.name_en
            self.loc.country_ru = self.data.sity.country_ru
            self.loc.country_en = self.data.sity.country_en
            self.loc.save()
        else:
            pass

        return super(StatView,self).get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super(StatView,self).get_context_data(**kwargs)
        context["ip"]=self.ip
        context["data"]=self.loc
        return context

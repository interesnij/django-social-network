# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()


response = requests.get(url= "http://api.sypexgeo.net/J5O6d/json/91.239.184.244")
print(response)
data = response.json()

sity = data['city']
region = data['region']
country = data['country']
loc.city_ru = sity['name_ru']
loc.city_en = sity['name_en']
loc.city_lat = sity['lat']
loc.city_lon = sity['lon']
loc.region_ru = region['name_ru']
loc.region_en = region['name_en']
loc.country_ru = country['name_ru']
loc.country_en = country['name_en']
loc.phone = country['phone']

print(data)

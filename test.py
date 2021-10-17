# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()


response = requests.get(url= "http://api.sypexgeo.net/J5O6d/json/91.239.184.244")
data = response.json()

print(data)

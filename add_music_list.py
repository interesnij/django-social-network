# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django, json, requests

django.setup()

import soundcloud
from music.models import *
from PIL import Image


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')


response = requests.get("https://api.soundcloud.com/resolve?url=https://soundcloud.com/discover/sets/charts-trending:all-music:ru&client_id=dce5652caa1b66331903493735ddd64d")
data = response.json()

if data:
    print(data)
    #print(data['uri'])
    #print(data['duration'])
    #print(data['permalink_url'])

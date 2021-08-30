# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

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
from datetime import datetime, date, time
import json, requests

data= None

response = requests.get(url= "https://api.soundcloud.com/playlists?url=https://soundcloud.com/eliana-cogine/sets/musicas-relaxantes&client_id=dce5652caa1b66331903493735ddd64d")
#data = response.json()

print(response.collection)

if data:
    for track in data['tracks']:
        print(track)

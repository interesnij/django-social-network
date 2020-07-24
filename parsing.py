# -*- coding: utf-8 -*-
from locale import *
import sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

import soundcloud
from music.models import *
from datetime import datetime, date, time
import json, requests


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')

response = requests.get(url= "https://api.soundcloud.com/resolve?url=https://soundcloud.com/rehan-khan-55/sets/meditation&client_id=dce5652caa1b66331903493735ddd64d")
data = response.json()

if data:
    for track in data['tracks']:
        track_genre = track['genre'].replace("'", '')
        print(track_genre)

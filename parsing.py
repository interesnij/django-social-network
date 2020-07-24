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


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
#page_size = 200
genres_list = SoundGenres.objects.values('name')
genres_list_names = [name['name'] for name in genres_list]

permalink_url = 'https://soundcloud.com/its-jezika-bruh/sets/chillax-mood'
permalink_url.replace("\\?", "%3f")
permalink_url.replace("=", "%3d")
permalink_url.replace("/", "%2F")
permalink_url.replace(":", "%3A")

list = SoundList.objects.get(uuid='b5c130a2-4c49-4341-9b7e-bc46f5fdc814')

start = 0
end = 20

playlist = client.get('/playlists/2050462')

if playlist:
    print (track[0])
    for track in playlist.tracks:
        print (track['title'])

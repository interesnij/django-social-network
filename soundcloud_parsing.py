# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()

import soundcloud
from music.models import SoundParsing


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
all_tracks = client.get('/tracks', order='created_at', limit=page_size, linked_partitioning=1)
for user in users.collection:
    SoundParsing.objects.create(title=user.title)
while all_tracks.next_href != None:
    all_tracks = client.get(all_tracks.next_href, order='created_at', limit=page_size, linked_partitioning=1)
    for user in users.collection:
        SoundParsing.objects.create(title=user.title)

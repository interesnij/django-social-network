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
genres_list = SoundGenres.objects.values('name')
genres_list_names = [name['name'] for name in genres_list]

permalink_url = 'https://soundcloud.com/its-jezika-bruh/sets/chillax-mood'
permalink_url.replace("\\?", "%3f")
permalink_url.replace("=", "%3d")
permalink_url.replace("/", "%2F")
permalink_url.replace(":", "%3A")

list = SoundList.objects.get(uuid='44984459-abc3-4838-af63-7b1b4fe78b20')

start = 0
end = 20

genres_list = SoundGenres.objects.values('name')
genres_list_names = [name['name'] for name in genres_list]
response = requests.get(url= "https://api.soundcloud.com/resolve?url=https://soundcloud.com/timpietrusky/sets/super-hot-shit&client_id=dce5652caa1b66331903493735ddd64d")
data = response.json()
print(data)

if data:
    for track in data['tracks']:
        created_at = track['created_at']
        created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

        if track['description']:
            description = track['description'][:500]
        else:
            description = None
        track_genre = track['genre'].replace("'", '')
        print(track_genre)

        try:
            new_track = SoundcloudParsing.objects.get(id=track['id'])
        except:
            if track['genre'] and track['genre'] in genres_list_names:
                genre = SoundGenres.objects.get(name=track_genre)
                new_track = SoundcloudParsing.objects.create(id=track['id'],
                                                        artwork_url=track['artwork_url'],
                                                        created_at=created_at,
                                                        description=description,
                                                        duration=track['duration'],
                                                        genre=genre,
                                                        title=track['title'],
                                                        uri=track['uri'],
                                                        release_year=track['release_year'])
                list.players.add(new_track)

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

    for track in playlist.tracks:
        created_at = track['created_at']
        created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')

        if track['description']:
            description = track['description'][:500]
        else:
            description = None
        if track['genre'] in genres_list_names:
            genre = SoundGenres.objects.get(name=track['genre'].replace("'", '') )
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

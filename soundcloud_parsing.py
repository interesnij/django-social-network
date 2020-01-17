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
page_size = 200
genres_list = SoundGenres.objects.values('name')
genres_list_names = [name['name'] for name in genres_list]

list_2_1 = [
"2 AM Club feat. Big Sean & Dev",
"2 Brorhers On The 4th Floor",
"2 Chainz",
"2 Fabiola",
"2 Faced Funks",
"2 For Love",
"2 Limits",
"2 Ontrack",
"2 Ontrack feat. Yolanda",
"2 Play",
"2 Unlimited",
"2 Ляма feat. Zivert",
"2 Маши",
"2-4 Grooves",
"2-SidE",
"2+2",
"2011stress",
"20th Century Steel Band",
"21 Savage",
"220 KID & Gracey",
"23:45",
"24 K",
"24/7",
"24hrs",
"24kGoldn feat. Lil Tjay",
"25-17",
"25/17",
"2AM Club",
"2B",
"2Boys",
"2BT Sound feat. Nadia",
"2Choice feat. Jakub Ondra",
"2Colourz",
"2D",
"2Elements",
"2fashion",
"2Fate & Nadya Tert",
"2G",
"2Hat",
"2Hillz feat. Dikla Elias",
"2IT",
"2Kool",
"2nd Phase",
"2nd Room",
"2NE1",
"2Night",
"2OYA",
"2pac",
"2pointS",
"2raumwohnung",
"2rbina 2rista",
"2Special",
"2sunny",
"2wice Shye feat. Kimosabe",
"2XS",
]

litera = SoundSymbol.objects.get(name="2")

count = 0

for tag in list_2_1:
    tracks = client.get('/tracks', q=tag, limit=page_size, linked_partitioning=1)
    if tracks:
        for track in tracks.collection:
            created_at = track.created_at
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            if track.description:
                description = track.description[:500]
            else:
                description=None
            try:
                SoundcloudParsing.objects.get(id=track.id)
            except:
                if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                    try:
                        self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                    except:
                        self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                    genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                    new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
                count = count + 1
        while tracks.next_href != None and count < 2000:
            tracks = client.get(tracks.next_href, limit=page_size, linked_partitioning=1)
            for track in tracks.collection:
                created_at = track.created_at
                created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                if track.description:
                    description = track.description[:500]
                else:
                    description=None
                try:
                    SoundcloudParsing.objects.get(id=track.id)
                except:
                    if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                        try:
                            self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                        except:
                            self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                        genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                        new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

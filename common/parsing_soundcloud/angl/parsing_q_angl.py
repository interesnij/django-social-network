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

q_rus_list_1 = [
"Q Machette feat. Bobby V",
"Q o d e s feat. Athena",
"Q-Sign feat. K.O.",
"Qadance",
"QAMI",
"Qaran feat. R3hab",
"Qleo feat. Lazee",
"Qmir",
"Qobee & Raikhana Mukhlis",
"Qobee feat. Jamaru",
"Qoma",
"Qontrast",
"QQ feat. Major Lazer & Swick",
"QQUN",
"Quality Control feat. Lil Baby & DaBaby",
"Quando Rondo feat. A Boogie Wit Da Hoodie & 2 Chainz",
"Quartissimo",
"Quavo & Saweetie",
"Quavo feat. Madonna & Cardi B",
"QUB",
"Quba",
"Qubicon",
"Que",
"Queen",
"Queen Bicycle Race",
"Queen Latifah",
"Queen Of Hearts",
"Queens",
"Queensberry",
"Queensley Felix",
"Quentin Mosimann",
"Quentyn",
"Quest Pistols",
"Quickstaff",
"Quico M.",
"Quiet Riot",
"Quietdrive",
"Quigley",
"Quincy Jagher",
"Quincy Jones",
"Quinn Lewis",
"Quinn XCII",
"Quintino",
"Quique Tejada feat. Monica Guech",
"Quix",
"Qulinez",
"Quman feat. Emily Kane",
"Qunst",
"Qveen Herby",
"Qwote",
"QZB",
]

litera = SoundSymbol.objects.get(name="Q")

count = 0

for tag in q_rus_list_1:
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
                Music.objects.get(id=track.id)
            except:
                if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                    try:
                        self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                    except:
                        self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                    genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                    new_track = Music.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
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
                    Music.objects.get(id=track.id)
                except:
                    if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                        try:
                            self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                        except:
                            self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                        genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                        new_track = Music.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

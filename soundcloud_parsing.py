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

x_rus_list_1 = [
"X Ambassadors",
"X Lovers",
"X Stress",
"X-Ander",
"X-Cess!",
"X-Change feat. Jimmy Burney",
"X-Fade",
"X-Hard",
"X-Killer",
"X-Mode and Dj Nil",
"X-Pander",
"X-Perience",
"X-Pression",
"X-Stylez & Two-M feat. Pedro Rodrigues",
"X-Tension",
"X-treme",
"X-Unicum feat. Margo Raj",
"X-Vertigo & Renco feat. Tab",
"Xaanti",
"Xamm",
"Xan Griffin",
"Xan Young",
"Xana",
"Xandee",
"Xandl",
"Xandra",
"Xandria",
"Xandro",
"Xanwow",
"Xav feat. Akon",
"Xavi Alfaro",
"Xavier Dunn",
"Xaxa",
"XB & Linnea Schossow",
"Xcho",
"Xclent",
"XDT feat. Cina",
"Xemplify",
"Xen feat. L Loko",
"Xenia Ghali",
"Xenianew",
"XES",
"Xeuphoria feat. Charlotte Haining",
"Xeya",
"Xhensila",
"Xian & The Entranced",
"Xie",
"Xilent",
"xKore feat. Gravity",
"XLDeluxe",]

x_rus_list_2 = [
"Xmas Bells of the Caribbean",
"Xmas Lounge Project",
"XO feat. James Chatburn",
"XO feat. Leo Kalyan",
"XoDa feat. Terry",
"XOMA",
"Xonia",
"XOV",
"Xpectra",
"Xristina Salti",
"Xriz",
"Xroyce",
"XS",
"XSO",
"Xstay",
"Xten feat. Angelika",
"XTM feat. Annia",
"XtriM",
"XTV",
"Xuman",
"Xuso Jones",
"XX FAM",
"Xxl",
"XXXTentacion",
"XY&O",
"XYconstant",
"XYLO",
"Xyloo",
"Xyphon",
"Xypo feat. A-Sho",
"Xzaltacia",
"Xzibit",
]

litera = SoundSymbol.objects.get(name="X")

count = 0

for tag in x_rus_list_2:
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


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

я_rus_list_1 = [
"Яак Йоала",
"Яжевика",
"Яжевика & GASpromo",
"Яжевика & L'One",
"Як-40",
"Яков Кирсанов",
"Яков Самодуров",
"Яковлев",
"Ямайцы & EYA",
"Ямалая",
"Ямыч (Восточный Округ) feat. Gipsy King & Liman",
"Ян Гарсэль & Egor Rezanov",
"Ян Глори",
"Ян Гэ",
"Ян Джамилович",
"Ян Женчак",
"Ян Ларри",
"Ян Маерс",
"Ян Марти",
"Ян Марти feat. AmaMama",
"Ян Райбург",
"Ян Соболев",
"Ян Степанов & Роман Ларин",
"Ян Табачник",
"Ян Ураган",
"Ян Френкель",
"Ян Ярош",
"Яна Berd",
"Яна Батаева",
"Яна Башкирева",
"Яна Брилицкая",
"Яна Вайновская",
"Яна Вереск",
"Яна Кошкина",
"Яна Латыпова",
"Яна Моисеева",
"Яна Павлова",
"Яна Редько",
"Яна Романова",
"Яна Соломко",
"Яна Соуле",
"Яна Томаева",
"Янковский feat. Richie Palmero & H1GH",
"Янковский и H1GH",
"ЯрмаК",
"Яросlove",
"Ярослав Евдокимов",
"Ярослав Калинин",
"Ярослав Кузнецов",
"Ярослав Сумишевский",
"Ярослав Щекланов",
"Ярослава Руденко",

]

litera = SoundSymbol.objects.get(name="Я")

count = 0

for tag in я_rus_list_1:
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
                    new_track = Music.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, description=description, title=track.title, uri=track.uri, release_year=track.release_year)
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
                        new_track = Music.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, description=description, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

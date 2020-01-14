
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

х_rus_list_1 = [
"Х.О.Х",
"Хаак feat. Dino Mc-47",
"Хабиб & Артем",
"Хабиб Шарипов",
"Хава",
"Хади",
"Хали-Гали",
"Хамелеон",
"Хамиль (Каста)",
"Хамиль и Змей (Каста)",
"Ханар",
"Ханна & Alex Shik",
"Ханна feat. DJ Цветкоff",
"Ханна feat. Luxor",
"Ханна Голышева",
"Ханна Маликова",
"Ханна Монтана 2",
"Ханчик",
"ХаП feat. Asscol",
"Харизмо & Анжелика Андерсон",
"Харламыч",
"Хасбулат Рахманов",
"Хачатурян",
"Хаш (Нush)",
"Хвост",
"Хедлайнер",
"Хипинуза",
"ХиппиПаНК",
"Хиро",
"ХМАО86",
"ХолодильНИК BAND",
"Холодно",
"Холостяк Максим",
"Холостячки",
"Хор Алтайского Края и Доминик Джокер",
"Хор Звёзд",
"Хор Им. Пятницкого",
"Хор Имени Пятницкого",
"Хор Русской Песни ВРК",
"Хор Турецкого",
"Хостел",
"Храмыч",
"Христина Соловій",
"Хроник ОМ. feat. Порох",
"Хрустальный Дождь",
"ХТБ",
"Хулиганы",
"Хурма Project",
"Хуршида",
"Хэллоуин",
]

litera = SoundSymbol.objects.get(name="Х")

count = 0

for tag in х_rus_list_1:
    tracks = client.get('/tracks', q=tag, limit=page_size, linked_partitioning=1)
    if tracks:
        for track in tracks.collection:
            created_at = track.created_at
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            if track.description:
                description = track.description[:500]
            try:
                SoundcloudParsing.objects.get(id=track.id)
            except:
                if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                    try:
                        self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                    except:
                        self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                    genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                    new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, description=description, title=track.title, uri=track.uri, release_year=track.release_year)
                count = count + 1
        while tracks.next_href != None and count < 2000:
            tracks = client.get(tracks.next_href, limit=page_size, linked_partitioning=1)
            for track in tracks.collection:
                created_at = track.created_at
                created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                if track.description:
                    description = track.description[:500]
                try:
                    SoundcloudParsing.objects.get(id=track.id)
                except:
                    if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                        try:
                            self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                        except:
                            self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                        genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                        new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, description=description, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

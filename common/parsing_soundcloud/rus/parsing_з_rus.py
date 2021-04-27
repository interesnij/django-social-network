
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

з_rus_list_1 = [
"За Полк",
"Забытый Женя",
"Заир feat. Джиос",
"Закир Салаватов",
"Залина Бостанова",
"Залина Лафишева",
"Заліско",
"Замира Дандамаева",
"Зануда (Centr)",
"Зануда feat. Angelina Rai",
"Запрещенные Барабанщики",
"Зара Долуханова",
"Зара и Дживан Гаспарян",
"Зарина Бугаева",
"Зарина Тилидзе",
"Зарипхан",
"Зарисовка",
"ЗАРС",
"Захар Насыров",
"Захаркин Руслан",
"Зачарованная",
"Звезды feat. ChinKong",
"Зверев Сергей and Непоседы",
"Звери",
"Здесь Наш Дом",
"Здоровье",
"Здравствуй, Песня",
"Зеваров",
"Зелим Бакаев",
"Земляне",
"Земфира",
"ЗЕНА",
"Зеновей Джебский",
"Зимовье Зверей",
"Зина Куприянович",
"Зиновий Бельский",
"Злаки & Мэнчестер",
"Злата Огневич",
"Златаслава",
"Злой ЛиC & ПодZемка",
"Змей (Каста)",
"Знак Четырёх",
"Зодиак",
"Золотое кольцо",
"Золушка",
"Зомб",
"Зона Лирики и Мурат Тхагалегов",
"Зорик",
"Зорик и Боря",
"Зорро",
"Зоя Левада",
"Зульфия Гаджиева",
"Зураб Соткилава",
]
litera = SoundSymbol.objects.get(name="З")

count = 0

for tag in з_rus_list_1:
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

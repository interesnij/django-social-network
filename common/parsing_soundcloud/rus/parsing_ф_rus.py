
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

ф_rus_list_1 = [
"Фазиле Ибраимова",
"Фактор-2",
"Факультеtt",
"Фанки",
"Фанкфары",
"ФанкЭйнштейн",
"Фарбэль",
"Фариз Мамедов",
"Фарт BZ",
"Фати Царикаева",
"Фатима Гаглоева",
"Фатима Дзибова",
"Фатима Дзыбова",
"Федерация",
"Фёдор Чистяков feat. Татьяна Буланова",
"Фёдор Шаляпин",
"Федосей",
"Федя Карманов",
"Феликс Луцкий",
"Феликс Макиев",
"Феллини",
"Ференц Лист",
"Феретти",
"Фидель",
"Филипп Киркоров",
"Филипп Флэйер",
"Философский Парень",
"ФинадеEV",
"Финес И Ферб",
"Фир",
"ФирТоф",
"Фирэль",
"Фишер feat. Zak",
"Фіолет",
"ФлайzZzа",
"Флешбэк & SLeiJ Mista",
"Фли",
"Флорида",
"Флоу Мо & Настя Крайнова",
"Фолиант Mc",
"Фомин Дмитрий",
"Фон Фортэ",
"Формула любви",
"Фортуна",
"Форум",
"Фрай",
"Франц Йозеф Гайдн",
"Франц Шуберт",
"Франциско",
"Френдзона",
"Френды",
"Фридерик Шопен",
"Фриске Ж and Таня",
"Фристайл",
"Фруктовый Кефир",
"Фрукты",
"Фуджи",
"Фьёрди",
]

litera = SoundSymbol.objects.get(name="Ф")

count = 0

for tag in ф_rus_list_1:
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

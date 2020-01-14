
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

э_rus_list_1 = [
"ЭffekT",
"ЭGO",
"ЭLTИ",
"Эva Voice",
"Эвелина Блёданс и Виктор Тартанов",
"Эд Р.Э.Й. Родионов",
"Эд Шульжевский",
"Эдд & Карина Крит",
"Эддисон feat. КЕДО & H1GH",
"Эдем",
"Эдик Салонский",
"Эдита Пьеха",
"Эдмунд Шклярский и Калинов Мост",
"ЭдО feat. Aй-Ман",
"Эдо Барнаульский",
"Эдуард Видный",
"Эдуард Дядюра",
"Эдуард Изместьев",
"Эдуард Изотов",
"Эдуард Курганский",
"Эдуард Лабковский",
"Эдуард Малов",
"Эдуард Подгорный",
"Эдуард Романюта",
"Эдуард Хиль",
"Эдуард Хуснутдинов",
"Эдуард Шенфельд",
"Эдуард Шилец",
"Эдуард Ярославцев",
"Эй Кей feat. SingaDi",
"Эймакс",
"Эймакс & Darom Dabro",
"ЭЙЯ",
"ЭКSТАZ",
"Эклипс",
"ЭКС ББ",
"Экс-Президенты",
"Экштайн",
"Эланея",
"Элано feat. ChipaChip",
"Элвин Грей",
"Электра (Лера Туманова)",
"Электроклуб",
"Электрошок",
"Элемент",
"Элен",
"Элина Чага",
"Элина Чага и Антон Беляев",
"Элис",
"ЭлКик & ЭленаВек",
"Элла Лефтерова",
"Эллаи",
"Эллей",
"Эллен",
"Элли",
"Эльбрус Джанмирзоев",
"Эльгюн Бадалов",
"Эльдар Артист",
"Эльдар Артист и Ирэна Ари",
"Эльдар Бабаев",
"Эльдар Далгатов",
"Эльмира Калимуллина",
"ЭльТино & T1One",
"Элэм",
"Элэндж feat. Владимир Винс",
"ЭмДжиЭл",
"Эмили",
"Эмиль и Друзья",
"Эмиль Кадыров",
"Эмине Зиадинова",
"Эмкиро feat. Дима Карташов",
"Эмма М",
"Эмма М feat. Миша Марвин",
"Эмси Нэнси",
"Эмсти feat. Comein",
"Энвер Измайлов",
"Энвер Каримов",
"Энвер Каримов feat. Kanvic",
"Эндже",
"Энди Картрайт",
"Энди Рид feat. Chitto",
"Эндигма",
"Эндигма & ALI",
"Эндоген feat. Dante",
"Эндрю К",
"Эндрю Фишер",
"Эндшпиль",
"Энкиро",
"Эннио Марриконе",
"Эр Джи",
"Эра Канн feat. Саша Чест",
"Эрика (Еріка)",
"Эрика и Алексей Матиас",
"Эрика Лундмоен",
"Эрика Сытник",
"Эрика Ферфис",
"Эротический саксофон",
"Эсер feat. Цепкий",
"Эскизы",
"Эсчевский",
"Эффект Бабочки",
"Эхо",
"Эшнайт (Eshnight)",
"Эштар",

]

litera = SoundSymbol.objects.get(name="Э")

count = 0

for tag in э_rus_list_1:
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

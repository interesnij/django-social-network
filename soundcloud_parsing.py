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

б_rus_list_1 = [
"Баnzай",
"Баnzай & Марик Вкураже",
"Бабек Мамедрзаев",
"Багз, Майк",
"Базилио",
"Базиль",
"Балаган Лимитед",
"Балагуры",
"Балкаров Алим",
"Банд'Эрос",
"Банда Андрюха",
"Банкес",
"Банума",
"Барбара",
"Барбарики",
"Барби Коктейль",
"БарДак",
"Барни и Лёня",
"Барто",
"Барыкин Александр",
"Басков Николай",
"Басота",
"Баста",
"Баталия",
"Батишта",
"Батыр",
"Батыр Шукенов",
"Баяна",
"Бедуин",
"Без Билета",
"Без Нот",
"Без Обмежень",
"Без Пароля",
"Без Пятнадцати Осень",
"Без чувств",
"Белая Гвардия",
"Белки на Акации",
"Белое Золото",
"БезПяти-4",
"Белое солнце пустыни",
"Беломорканал",
"Белоснежка И Семь Гномов",
"Белый",
"Белый Бим, черное ухо",
"Белый День",
"Белый Орел",
"Белый Свет",
"Берегись автомобиля",
"Берёзкин Ян",
"Беркут",
"Би-2",
"Биг Бэта",
"Бигуди Шоу",
"Билан Дима",
"Билик",
"БИС",
"Бис и КуБа",
"Биссектриса",]
б_rus_list_2 = [
"Битва В Пути",
"Блажин",
"Блестяшки",
"Блестящие",
"Блокбастер",
"Блокпост",
"Блонди",
"Блондинка КсЮ",
"Блудливый Либерал",
"Боби",
"Боботов Кук",
"Бобровский Сергей",
"Бобры",
"Богдан",
"Богдан Галий",
"Богдан Губарь",
"Богдан Дюрдь",
"Богдан Титомир",
"Богдан Шувалов",
"Богодар Которович",
"Божья Коровка",
"Большая Перемена",
"Больше Всех",
"Больше Гонора",
"Большой детский хор",
"Большой Хор Вр",
"Боник",
"Бордо",
"Борис Агаджанян",
"Борис Берг",
"Борис Браун",
"Борис Вахнюк",
"Борис Гребенщиков",
"Борис Грим",
"Борис Драгилев",
"Борис Иванов",
"Борис Логинов",
"Борис Моисеев",
"Борис Новичихин",
"Борис Рубашкин",
"Борис Тарасевич",
"Борис Тихонов",
"Борис Шварцман",
"Борис Шигин",
"Бородин Арсений",
"Браво",
"Браво и Маша Макарова (Маша И Mедведи)",
"Бразис",
"Бразис feat. StaffOnly",
"Брандо",
"Брат МС",
"Братец Медвежонок",
"Братубрат",
"Братья Борисенко",
"Братья Гаязовы",
"Братья Грим",
"Братья Поздняковы",
"Братья Жуковы",
"Брачелло",
"БРДК",
"Бригадный Подряд и Лусинэ Геворкян",
"Бриллиантовая рука",
"Бродвей",
"Бронс",
"Букатара",
"Буланова Татьяна",
"Булат Окуджава",
"Бумбокс",
"Бумер",
"Бурановские Бабушки",
"Бурито",
"Бурито и Ёлка",
"Бутырка",
"БЫБА",
"Быть Собой",
"Бьянка",
"БЭ ПЭ",
"Бэби-Шлягер",
"Бэмби",
]



litera = SoundSymbol.objects.get(name="Б")

count = 0

for tag in б_rus_list_2:
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
                    new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, description=description, title=track.title, uri=track.uri, release_year=track.release_year)
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
                        new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, description=description, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

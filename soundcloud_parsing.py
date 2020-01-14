
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

ю_rus_list_1 = [
"Ю-GranD",
"Ю-Питер",
"Юджин",
"Южная Башня Сalor.v feat. F.F.",
"ЮжныйБруклин feat. Кажэ Обойма",
"ЮКОН",
"Юлана",
"Юлиана Караулова",
"Юлиана Раевская",
"Юлиана Ян",
"Юлианна Караулова",
"Юлианна Лукашева",
"Юлий Ким",
"Юлика и Dj Слон",
"Юлия Holod",
"Юлия Nelson",
"Юлия Адамчук",
"Юлия Алексанова",
"Юлия Альбах и Дмитрий Мазур",
"Юлия Андреева",
"Юлия Артёмова",
"Юлия Бардаш",
"Юлия Беккер",
"Юлия Берген",
"Юлия Беретта",
"Юлия Бойко",
"Юлия Валова",
"Юлия Ватраль",
"Юлия Войс",
"Юлия Волгина",
"Юлия Волкова (Julia Volkova)",
"Юлия Грозная",
"Юлия Губанова",
"Юлия Дакс",
"Юлия Демьянова",
"Юлия Дробот",
"Юлия Думанская",
"Юлия Есина",
"Юлия Жукова",
"Юлия Кан",
"Юлия Ковальчук",
"Юлия Коган",
"Юлия Коган и Андрей Князев",
"Юлия Кремер",
"Юлия Линд",
"Юлия Максимчук",
"Юлия Митюнина",
"Юлия Михальчик",
"Юлия Морозова",
"Юлия Началова",
"Юлия Началова feat. Mc Jamay",
"Юлия Нельсон",
"Юлия Оксанич",
"Юлия Пак",
"Юлия Подпорина",
"Юлия Проскурякова",
"Юлия Пушман",
"Юлия Райнер",
"Юлия Романовская и Юрий Никитюк",
"Юлия Савичева",
"Юлия Самойлова",
"Юлия Сандерс",
"Юлия Сендерс",
"Юлия Ступак",
"Юлия Феста и Андрей Гражданкин",
"Юлия Хоменко",
"Юлия Хусаинова",
"Юлия Чичерина",
"Юлия Шереметьева",
"Юлія Лорд",
"Юля Волкова",
"Юля Годунова",
"Юля Ив",
"Юля Ковальчук",
"Юля Нова",]

ю_rus_list_2 = [
"Юля Паго (Pago)",
"Юля Потехина",
"Юля Прадо",
"Юля Райнер",
"Юля Саваичева",
"Юля Савичева",
"Юля Савичева И Джиган",
"Юля Чернова",
"Юля Шатунова",
"Юля Шатунова feat. Jeroni",
"Юность Внутри",
"Юра Магомаев",
"Юра Неплохой и Антон Зацепин",
"Юра Титов",
"Юра Хаимов",
"Юра Шатунов",
"Юрашъ",
"Юрий EzzeN",
"Юрий Антонов",
"Юрий Белошевский",
"Юрий Богатиков",
"Юрий Богданов",
"Юрий Визбор",
"Юрий Гарин",
"Юрий Герляйн",
"Юрий Гора",
"Юрий Гриценко",
"Юрий Гуляев",
"Юрий Деденёв",
"Юрий Дранга",
"Юрий Забродин",
"Юрий Казаков",
"Юрий Калашников",
"Юрий Кармов",
"Юрий Ким",
"Юрий Комар",
"Юрий Кость",
"Юрий Кочановский",
"Юрий Кукин",
"Юрий Куксин",
"Юрий Лаврушин",
"Юрий Левитан",
"Юрий Лоза",
"Юрий Магомаев",
"Юрий Маковей",
"Юрий Мещеряков",
"Юрий Николаев",
"Юрий Никулин",
"Юрий Олейников",
"Юрий Охочинский",
"Юрий Плотников",
"Юрий Прибылов",
"Юрий Рогов",
"Юрий Сандик",
"Юрий Смыслов",
"Юрий Спиридонов",
"Юрий Титов",
"Юрий Титов и Монокини",
"Юрий Уральский",
"Юрий Федотов & A-Net",
"Юрий Филоненко",
"Юрий Хаимов",
"Юрий Цаплин",
"Юрий Чичков",
"Юрий Шатунов",
"Юрий Шахнов",
"Юрий Шевчук",
"Юрий Шилов",
"Юрий Якушев",
"Юрий Ярыгин",
"Юркеш",
"ЮрКисс",
"Юта",

]

litera = SoundSymbol.objects.get(name="Ю")

count = 0

for tag in ю_rus_list_1:
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

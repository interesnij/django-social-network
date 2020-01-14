
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

г_rus_list_1 = [
"Габриэль",
"Гаврик & Олександр Положинський",
"ГадЖеТы",
"Гайдай",
"Гайдамаки",
"Гайк",
"Гайтана",
"Галактика",
"Галамарт",
"Галамартовна",
"Галина",
"Галина Боб",
"Галина Журавлёва (Журга)",
"Галина Комиссарова",
"Галина Комиссарова и Михаил Кармаш",
"Галина Ненашева",
"Галина Хомчик",
"Галина Шапкина",
"Галина Юдина",
"Галя Боб",
"Галя Журавлёва",
"Галямин Сергей feat. Samoel",
"Гамора",
"Ганвест",
"Гансэлло",
"Гардемарины Вперед",
"Гари Гудини feat. M.J. Marley (Стиль Бандит)",
"Гарик Кричевский",
"Гарик Мошенник & DJ Favorite",
"Гарик Погорелов",
"Гарик Сукачёв",
"Гарик-Ниагарик",
"Гармония",
"Гарри Польский",
"Гарри Топор",
"Гаррий Манукян",
"Гаттака",
"Гаяне Аракелян",
"Гейдар Багиров",
"Гела Гуралиа",
"Гельдуш Османов",
"Гена Гром",
"Гена Селезнев",
"Геннадий Белов",
"Геннадий Виноградов",
"Геннадий Витер",
"Геннадий Вяземский",
"Геннадий Гладков",
"Геннадий Горелик",
"Геннадий Жаров",
"Геннадий Иванцов",
"Геннадий Лясковский",
"Геннадий Парыкин",
"Геннадий Пугачев",
"Геннадий Ура",]

г_rus_list_2 = [
"Георгий Колдун",
"Георгий Лысенко",
"Георгий Свиридов",
"Гера Герасимов",
"Гера Грач",
"Геракл",
"Герб feat. DJ Jedy",
"Герман Грач",
"Герман Титов",
"Герман Чепелянский",
"Герман Черных",
"Герои",
"Герои и Belka",
"Герои Комиксов",
"Герр Антон",
"Гетман",
"ГЕЦе",
"Гига",
"Гильzа",
"Главная Роль",
"Гладков Григорий",
"Глаза",
"Гламур",
"Глеб Матвейчук",
"Глюк’oza",
"Глюкоzа",
"Глюкоза",
"Гоголь-Моголь",
"Год Змеи",
"Голди",
"Голод",
"Голубые Береты",
"Гордей Белов",
"Город 312",
"Горшенев",
"Горячие головы",
"Горячий Шоколад",
"Горячий шоколад и Тринити",
"Гослинг",
"Гости Из Будущего",
"Гостья из будущего",
"Гоша Style",
"Гоша Грачевский",
"Гоша Куценко",
"Гоша Матарадзе",
"гр LIFE",
"гр. Бумер",
"гр. Пропорции feat. Кэти Эбель",
"Градусы",
"Гранат",
"Гранды",
"Граф Гагарин",
"Гребенщиков Михаил",
"Грейс",
"Гречка",
"Грешник",
"Грибы",
"Григ",
"Григорий Герасимов",
"Григорий Гладков",
"Григорий Данской",
"Григорий Есаян",
"Григорий Лепс",
"Григорий Филь",
"Григорий Юрченко",
"Грин Данилов",
"Гринджоли",
"Гринскрин",
"Гриша Гост & Глеб Калюжный",
"Гриша Заречный",
"Гриша Петров",
"Грозовой Перевал",
"Грот",
"Грузман",
"Группа 5 Плюс",]

г_rus_list_3 = [
"Группа F1",
"Группа Ferramon",
"Группа Fm",
"Группа H2O",
"Группа PLAY",
"Группа Radио",
"Группа А.Т.А.С.",
"Группа Аня",
"Группа Братва",
"Группа Весна",
"Группа Владимир",
"Группа Евразия",
"Группа Запретка",
"Группа Колыма",
"Группа Круче Тучи",
"Группа Крылья",
"Группа Купажъ",
"Группа Лиц",
"Группа Маша Пирожкова",
"Группа Мира",
"Группа Мишель",
"Группа Мурkiss",
"Группа Навстречу Солнцу",
"Группа Одесса",
"Группа Олега Ястребова",
"Группа Онлайн",
"Группа Опаньки",
"Группа Панама",
"Группа ПМ",
"Группа Порт Петровск",
"Группа Р",
"Группа Регион 42 & Александр Кузнецов",
"Группа РЭДЛ?",
"Группа Ряженка",
"Группа Самоцветы",
"Группа Санкции",
"Группа Сентябрь",
"Группа Стаса Намина",
"Группа Улицы",
"Группа Централ",
"Гузель Уразова",
"Гузель Хасанова",
"Гульназ",
"Гурмэ",
"Гурченко and Dj Грув",
"Гусейн Гасанов",
"Гюльназ Гаджикурбанова",
]



litera = SoundSymbol.objects.get(name="Г")

count = 0

for tag in г_rus_list_1:
    tracks = client.get('/tracks', q=tag, limit=page_size, linked_partitioning=1)
    if tracks:
        for track in tracks.collection:
            created_at = track.created_at
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            try:
                SoundcloudParsing.objects.get(id=track.id)
            except:
                if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                    try:
                        self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                    except:
                        self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                    genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                    new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, stream_url=track.stream_url, title=track.title, uri=track.uri, release_year=track.release_year)
                count = count + 1
        while tracks.next_href != None and count < 2000:
            tracks = client.get(tracks.next_href, limit=page_size, linked_partitioning=1)
            for track in tracks.collection:
                created_at = track.created_at
                created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                try:
                    SoundcloudParsing.objects.get(id=track.id)
                except:
                    if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                        try:
                            self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                        except:
                            self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                        genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                        new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, stream_url=track.stream_url, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

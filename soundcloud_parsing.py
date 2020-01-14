
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

п_rus_list_1 = [
"П. Луспекаев",
"Павел Артемьев И Ирина Тонева",
"Павел Балтийский",
"Павел Беккерман",
"Павел Вишерский",
"Павел Воробьёв",
"Павел Данилов",
"Павел Кашин",
"Павел Козлов",
"Павел Красношлык",
"Павел Мах",
"Павел Михайлов",
"Павел Мурашов",
"Павел Нарочанский",
"Павел Павлецов",
"Павел Пиковский и Группа Хьюго",
"Павел Родни",
"Павел Соколов",
"Павел Фёдоров",
"Павел Федоров (Paulo)",
"Павел Филатов",
"Павел Филатов & Настя",
"Павел Филатов и группа Вне Зоны",
"Павел Чумаков",
"Павел Шевцов",
"Павел Шубин и Андрей Якиманский",
"Павла и Денис Ковальский",
"Павлентий Чернов",
"Павло Табаков",
"Пальчики Оближешь",
"Пан and Dino MC 47",
"Панакота",
"Панда feat. tompSON",
"Паола",
"Папины Дети",
"Пара нормальных",
"Пара Совпала",
"Параллельные",
"ПараТайн",
"Парень Из Союза",
"Пари",
"Парк Удовольствий",
"Паскаль",
"ПатриотЪ",
"Паук feat. Togga & Kvadrat",
"Паулина Андреева feat. Баста",
"Пацанка",
"Пацаны",
"Пачуля",
"Паша Proorok",
"Паша Вайти",
"Паша Захарчук",
"Паша Климат feat. Сюзанна Абдулла",
"Паша Ли",
"Паша Люмин и Даша Шувалова",
"Паша Мос",
"Паша Панамо",
"Паша Руденко",
"Паша Сли",
"Паша Цветомузыка",
"Паша Юдин",
"Пающие Трусы",
"Певица Афродита",
"Пелих Ангелина",
"Пепел Роза",
"Первая Zаповедь & Савва Тихий",
"Первая Zаповедь, Ahimas & Чак (M.Family)",
"Первый Контакт",
"Первый поворот",
"Песняры",
"Петкун, Голубев, Макарский",
"Петлюра",
"Петр Гара",
"Пётр Дранга",
"Петр Елфимов",]

п_rus_list_2 = [
"Петр Ильич Чайковский",
"Пётр Казаков",
"Петр Лещенко",
"Петр Налич",
"Петр Сергеев",
"Петя Черный",
"ПЗЖЕ feat. Рыбос",
"Пиджаков",
"Пикник",
"Пилот",
"Пиноккио",
"Пионерский Хор Им. В.У. Попова",
"Питер Пэн",
"Пицца",
"Пламя",
"Планета 90",
"Планка",
"Пластика",
"Платина",
"Плохиш",
"По Ту Сторону",
"По Фрейду",
"Под Одним Небом",
"ПодZемка",
"Подиум",
"Поднимаем Руки Вверх",
"Подпольная Траектория feat. Ahimas",
"Подруги",
"Подстрелов",
"Подъём!",
"Позитив and Напильник",
"Покахонтас",
"Полежаев",
"Полиграф ШарикOFF",
"Полина Богатикова",
"Полина Богусевич",
"Полина Буторина feat. DJ Groove",
"Полина Гагарина",
"Полина Гриффис",
"Полина Зизак",
"Полина Кузовкова (Pollykuu)",
"Полина Ростова",
"Полина Смолова",
"Полина Сокольская",
"Полина Соя",
"Полнолуние",
"Положительный Заряд",
"Полтергейст",
"Полумягкие",
"Полюса",
"Попанбэнд",
"ПопКорн",
"После 11",
"После Вчерашнего",
"Потапов Владимир",
"Потемковский",
"Потехин Бэнд",
"Потехин, Трэк и Блюз",
"Поющие вместе",
"Поющие трусы",
"Президент И Амазонка",
"Премьер-Министр",
"Приключения Мишек Гамми",
"Приключения Спин И Марти",
"Приключения Тигрули",
"Приключения Флика",
"Принцесса Авенью",
"Принцесса И Лягушка",
"Принцип (ZM)",
"Провинция 42 feat. Bizaro",
"Прогульщики",
"Продавцы Новостей",
"Проект Димac",
"Проект Жить",
"Проект Увечье",]

п_rus_list_3 = [
"Проект-22",
"Прокофьев",
"ПромЗона",
"Пропаганда",
"Пропорции",
"Проспект 64",
"Против Правил",
"Профессор Лебединский",
"Профилактика",
"Профсоюзный Ансамбль Песни И Пляски",
"Прохор Шаляпин",
"Психо",
"Птаха",
"Пугачева Алла",
"Пульсы",
"Пуля",
"Путевка В Жизнь",
"Пушкашу & Випи",
"Пыльца",
"Пьер Нарцисс",
"Пьера",
"Пэссо",
"Пятилетка",
"Пятница 13-е",
]

litera = SoundSymbol.objects.get(name="П")

count = 0

for tag in п_rus_list_2:
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

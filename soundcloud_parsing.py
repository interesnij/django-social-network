
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

е_rus_list_1 = [
"Е-30",
"Е. Нестеренко",
"Е. Семенова",
"Е2 Знакомы",
"Ева Амурова",
"Ева Анри",
"Ева Браун",
"Ева Бушмина",
"Ева Власова",
"Ева Новак",
"Ева Ост",
"Ева Польна",
"Ева Тимуш",
"Евгений Youjinn",
"Евгений Анегин и Юля Михальчик",
"Евгений Анисимов",
"Евгений Анисимов & SERPO",
"Евгений Бакшиев",
"Евгений Беляев",
"Евгений Бунтов",
"Евгений Виноградов",
"Евгений Воинов",
"Евгений Волконский",
"Евгений Воробьёв",
"Евгений Ворошилов",
"Евгений Град",
"Евгений Григорьев (Жека)",
"Евгений Гришковец и Бигуди",
"Евгений Дворянинов",
"Евгений Долгов",
"Евгений Жагалтаев",
"Евгений Замятин",
"Евгений Зачеславский",
"Евгений Илларионов",
"Евгений Кемеровский",
"Евгений Клепинин",
"Евгений Клячкин",
"Евгений Колос",
"Евгений Кондаков",
"Евгений Коновалов",
"Евгений Корн",
"Евгений Крылатов",
"Евгений Куневич",
"Евгений Лекс",
"Евгений Литвинкович",
"Евгений Лузин",
"Евгений Мальцев",
"Евгений Маргулис",
"Евгений Медведев",
"Евгений Минорский",
"Евгений Миха",
"Евгений Михель",
"Евгений Мошков",
"Евгений Нестеренко",
"Евгений Овсянников",
"Евгений Осин",
"Евгений Полянский",
"Евгений Попов",
"Евгений Рогов",
"Евгений Розман",
"Евгений Романтик",
"Евгений Росс",
"Евгений Рыбчинский",
"Евгений Сбитнев",
"Евгений Сидорук",
"Евгений Солодовников",
"Евгений Трофимов",
"Евгений Феклистов (Конец Фильма)",
"Евгений Чубик",
"Евгений Шкант",
"Евгений Юджин",
"Евгения Власова",
"Евгения Волконская",
"Евгения Дидюля",
"Евгения Долгова",]

е_rus_list_2 = [
"Евгения Карельская",
"Евгения Колпакова",
"Евгения Майер",
"Евгения Майер & Диана Видякина",
"Евгения Отрадная",
"Евгения Поликарпова",
"Евгения Смольянинова",
"Евгения Уфимская",
"Евро",
"Егиазар",
"Егор Krait",
"Егор Диких",
"Егор Кифес",
"Егор Крид & Валерия",
"Егор Крид feat. Arina Kuzmina",
"Егор Крид feat. Rakurs",
"Егор Крид feat. Мот",
"Егор Крид feat. Филипп Киркоров",
"Егор Крид vs. Alex Menco & Yonce",
"Егор Натс",
"Егор Сесарев",
"Егор Сесарев feat. Кравц",
"Егор Феникс",
"Егоров Вадим",
"Единое Братство feat. Kalash",
"Единое Братство feat. System Gold Krocodile",
"Единыйцелый",
"Единыйцелый feat. Иракли",
"Ежевика",
"Ейра",
"Екатерина Korol feat. Анна Калашникова",
"Екатерина Борзова",
"Екатерина Бужинская",
"Екатерина Гусева",
"Екатерина Данилова",
"Екатерина Дубровская",
"Екатерина Истомина",
"Екатерина Кадегрова",
"Екатерина Кокорина",
"Екатерина Матусова",
"Екатерина Павлова",
"Екатерина Печкурова",
"Екатерина Разумовская",
"Екатерина Семёнова",
"Екатерина Ульянова",
"Екатерина Чурина",
"Екатерина Шемякина",
"Елена Альтергот",
"Елена Бакурова",
"Елена Балакина",
"Елена Балашова",
"Елена Беляева",
"Елена Беркова",
"Елена Ваенга",
"Елена Василевская",
"Елена Васянина",
"Елена Воробей",
"Елена Галицына",
"Елена Гладких",
"Елена Глебова",
"Елена Гришанова",
"Елена Гудкова",
"Елена Дарк",
"Елена Елсакова",
"Елена Есенина",
"Елена Казанцева",
"Елена Камбурова",
"Елена Князева",
"Елена Кокорина",
"Елена Кузьмина",
"Елена Кукарская",
"Елена Ламур",
"Елена Лордес",
"Елена Максимова",
"Елена Мороз",]

е_rus_list_3 = [
"Елена Неклюдова",
"Елена Орлова",
"Елена Парфюм feat. DEYV IMPACT",
"Елена Решетняк",
"Елена Светлая",
"Елена Север",
"Елена Севостьянова",
"Елена Теплякова",
"Елена Терлеева",
"Елена Тишкова",
"Елена Хворостян",
"Елена Хмель",
"Елена Яловик",
"Елизавета Мармач",
"Елизавета Родина и Анна Родина",
"Елисей Михайлов & Сергей Горбацкий",
"Елка",
"Ёлочные Игрушки",
"Ена",
"Ерёмин",
"ЕрмакЪ",
"Есения",
"Есфирь",
"Ефим feat. Мария Кованцева",
"Ефим Шифрин",
"Ефрем Амирамов",
"Ефрем Флакс",
]


litera = SoundSymbol.objects.get(name="Е")

count = 0

for tag in е_rus_list_3:
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

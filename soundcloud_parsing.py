
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

л_rus_list_1 = [
"Л.Лядова И Н.Пантелеева",
"Лабиринт",
"Лава",
"Лаванда",
"Лавика",
"Лада Дэнс",
"Лада Дэнс и Брэндон Стоун",
"Лада Мишина",
"Лазурный берег",
"Лайма Вайкуле",
"Лакмус",
"Лама Сафонова",
"Ламма Андрей",
"Лампасы",
"Лана Клер",
"Лана Копей",
"Лана Луговая feat. TE",
"Лана Рэй feat. T.Y.",
"Лана Свит",
"Лана Шавлохова",
"Лапин Вячеслав",
"Лара Кроутс",
"Лара Фабиан, Игорь Крутой, Дживан Гаспорян",
"Лариса Голубкина",
"Лариса Гордъера",
"Лариса Гордьера",
"Лариса Грибалева",
"Лариса Долина",
"Лариса Закиева",
"Лариса Луста",
"Лариса Мондрус",
"Лариса Рождественская",
"Лариса Черникова",
"Ласковый Бык",
"Ласковый Май",
"Ласковый Шёпот",
"ЛАУД feat. Thomas Mraz",
"Лаурита",
"Лев Барашков",
"Лев Валерьяныч (L'One)",
"Лев Лещенко",
"Лев Тимашов",
"Лева Twice feat. Блик Papazz",
"Лёва Камский",
"Леван Горозия (L'One)",
"Левлис",
"Левон Морозов",
"Легион",
"Легостаев Константин",
"Леди И Бродяга",
"Лейся песня",
"Лейся, песня",
"Лёлё",
"Лель Катя",
"Лёля",
"Лена Бигус",
"Лена Бронская",
"Лена Волошина",
"Лена Гордеева",
"Лена Град",
"Лена Гранд",
"Лена Дарк",
"Лена Есенина & Mr VeN",
"Лена Катина",
"Лена Князева",
"Лена Максимова",
"Лена Перова",
"Лена Семенова",
"Лена Семенова и Илья Гуров",
"Лена Третьякова (Ранетки)",
"Лена Швец",
"Ленинград",
"Леона Аврелина",
"Леонид Агутин",
"Леонид Давыдов",]

л_rus_list_2 = [
"Леонид Иконников",
"Леонид Кострица",
"Леонид Минаев",
"Леонид Панов",
"Леонид Портной",
"Леонид Руденко",
"Леонид Сергеев",
"Леонид Телешев",
"Леонид Утесов",
"Леонид Фёдоров",
"Леонидыч",
"Леонсия Эрденко",
"Леопардо",
"Леприконсы",
"Лера Антипова",
"Лера Козлова",
"Лера Комлева",
"Лера Кондра",
"Лера Крик",
"Лера Массква",
"Лера Маяк",
"Лера Огонёк",
"Лера Туманова",
"Лера Шургалина",
"Лера Яскевич",
"Лерика Голубева",
"Лерика и Александр Ревва",
"Лесоповал",
"Леся Денисова",
"Леся Ярославская",
"Летать!",
"Летняя Магия",
"Лето",
"Летта",
"Летти",
"Летучий Голландец",
"Леуш Любич",
"Лёша Gs",
"Лёша KasPer",
"Лёша Маэстро",
"Леша Свик",
"Леша38",
"Леша7емь & MNR",
"Лигалайз",
"Лигейя",
"Лида Ком",
"Лидия",
"Лидия Аксенич",
"Лиза Small",
"Лиза Громова",
"Лиза и Наизнанку",
"Лиза Лукашина",
"Лиза Пурис",
"Лиза Хегай",
"Лиза Хопс & SERPO",
"Лиза Эванс",
"Лизабэт",
"Лика Стар",
"Лили Иванова",
"Лилиана Садовская",
"Лилия Леман",
"Лилия Месхи",
"Лилия Султанова",
"Лилия Шаулухова",
"Лило И Стич",
"Лиля Киш",
"Лина Мицуки",
"Лина Нова",
"Линда",
"Лион",
"Лип Лап",
"Лирика Улиц",
"Лицей",
"Лицо Под-Капюшоном feat. T1One",
"Лія Лі",]

л_rus_list_3 = [
"ЛОVI feat. Кошка",
"Лови",
"Ловушка Для Родителей",
"Лоза Юрий",
"Лолита Волошина",
"Лора Квинт и Максим Аверин",
"Лорена Сарбу",
"ЛОТОS",
"Лочи",
"Лоя",
"ЛСП",
"Луколя",
"Лунна",
"Лунный Пес",
"Луперкаль",
"Лэм Самоваров & Izzamuzzic",
"ЛюSea",
"Люба Альманн",
"Любаша & Николай Трубач",
"Любаша и Эвклид Кюрдзидис",
"Любо-Дорого",
"Любовные Истории",
"Любовь Попова",
"Любовь Успенская",
"Любовь Фоменко",
"Любовь Шепилова",
"Любэ",
"Людмила Горцуева & Анатолий Бетейко",
"Людмила Гурченко",
"Людмила Зыкина",
"Людмила Кононова",
"Людмила Лопато",
"Людмила Розум",
"Людмила Сенчина",
"Людмила Соколова",
"Людмила Шаронова",
"Люля Витрук",
"Люмьер",
"Люсьен",
"Люся Чеботина",
"Лютый Миkkи",
"Ля Миноръ",
"Ляля Жемчужная",
"Ляля Размахова",
"Ляля Рублева",
"Лям, Maxello",
"Лям, Гоша Матарадзе ft. Ян",
"Ляна Новак",
"Ляпис Трубецкой",
]

litera = SoundSymbol.objects.get(name="Л")

count = 0

for tag in л_rus_list_2:
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

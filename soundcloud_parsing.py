
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

т_rus_list_1 = [
"Т-134",
"Т.Т. feat. Сердце Дженнифер",
"Т9 feat. Panopticum Project",
"Т9 feat. Вне Времени",
"Та Сторона",
"ТАNИША",
"Табал & Pra(Killa'Gramm)",
"Табула Раса",
"Таврян",
"Таежный роман",
"Таис и Евгений Белый",
"Таисия Павенская",
"Таисия Повалий",
"Тайпан",
"Так Дорого Моему Сердцу",
"Такер",
"Такие Дела",
"Таких Миллион",
"Тамара Викберг",
"Тамара Гарибова",
"Тамара Гвердцители",
"Тамара Миансарова",
"Тамара Персаева",
"Тамара Саксина",
"Тамара Синявская",
"ТамДеМи",
"Тамерлан и Алена",
"ТАН_ХО",
"Танцы Минус",
"Таня BerQ",
"Таня Аверман и Семён Ланцет",
"Таня Антоник",
"Таня Буланова",
"Таня Ветринская и Павел Беккерман",
"Таня Геворгян",
"Таня Герман",
"Таня Дьяченко",
"Таня Дяченко",
"Таня Кондратенко",
"Таня Мамаева & Eugene Radionov",
"Таня Моль",
"Таня Мэр",
"Таня Панова (SUN Дали) и Алексей Воробьев",
"Таня Ромашкевич",
"Таня Северная",
"Таня Степанова",
"Таня Терешина",
"Таня Тишинская",
"Таня Тузова",
"Таня Ши",
"Таня Штерн и Александр Келеберда",
"Таня Юрская",
"Тараканы",
"Тарас Гаврик",
"Тарас Карпов",
"Тарас Курчик",
"Тати",
"Тату",
"Татьяна Анциферова & Лев Лещенко",
"Татьяна Баранова и Андрей Гоптарь",
"Татьяна Буланова",
"Татьяна Волощук",
"Татьяна Воржева",
"Татьяна Гончарова",
"Татьяна Жукова",
"Татьяна И Сергей Никитины",
"Татьяна Козловская",
"Татьяна Коннолли",
"Татьяна Копосова",
"Татьяна Коршук и Олег Баянов",
"Татьяна Котова",
"Татьяна Кузьмина",
"Татьяна Лихачёва",
"Татьяна Маргай",
"Татьяна Маркова",]

т_rus_list_2 = [
"Татьяна Морозова",
"Татьяна Недельская",
"Татьяна Овсиенко",
"Татьяна Осипова",
"Татьяна Пискарева",
"Татьяна Решетняк",
"Татьяна Рузавина & Сергей Таюшев",
"Татьяна Снежина",
"Татьяна Сорокина",
"Татьяна Тишинская",
"Татьяна Третьяк",
"Татьяна Тудвасева",
"Татьяна Чубарова",
"Татьяна Ширко",
"Татьяна Юрская & Наталья Нейт",
"Таша Белая",
"Таша Фролова",
"Тбили Тёплый",
"Твёрдый ЗнакЪ",
"ТвоиМурашки",
"Твой День",
"Твоя Молодость",
"Те100стерон",
"Теамо и Анри",
"Тельман Ибрагимов",
"Тёма Sirius",
"ТемирКош & Марьяна Саральп",
"Темиров Тимур",
"Тёмная Визия",
"Темча К. (Da Gudda Jazz) feat. Хофа",
"ТЕО",
"Теона Дольникова",
"Теона Нарикаева",
"Терёха",
"Территория Тишины",
"Тестостерович",
"Тет-А-Тет",
"Тетрис",
"Технология",
"Тигран Гарибян",
"Тилэкс",
"Тим Агрессор",
"Тима Белорусских",
"Тимси",
"Тимур Timbigfamily",
"Тимур Tемертей",
"Тимур Беноевский",
"Тимур Вагапов",
"Тимур Валеев",
"Тимур Дореми",
"Тимур Лехов",
"Тимур Ногаев",
"Тимур Рахманов",
"Тимур СПБ",
"Тимур Темиров",
"Тимур Темиров & Рада Рай",
"Тимур Темиров и Соня Муртазалиева",
"Тимур Шаов",
"Тина Кароль",
"Тина Корнет",
"Тина Кузнецова",
"Типси Тип",
"Титры",
"ТНМК",
"Токио",
"Толик Ershov",
"Тони Раут feat. Vit",
"Тони Рэй",
"Тони Спокойно",
"Тони Тонн",
"Тоня Матвієнко",
"Тор Сурис",
"Торба-на-Круче",
"Тося Чайкина",]

т_rus_list_3 = [
"Тотал"
"Точиловы",
"Тоша Мюллер и Александр Крейк",
"ТП БАРАДА (Булат, Нигатив (Триада), Реванш)",
"Трайсон",
"Трайсон feat. Kerin",
"Тренер feat. Ahimas",
"Треф feat. Greeza",
"Три Желания",
"Три Поросёнка",
"Три Пули",
"Триагрутрика",
"Тризэ",
"Тринадцать Строк",
"Трио S-Klass",
"Трио Реликт",
"Тритон",
"Триумф",
"Триши",
"Трое Молодых",
"Трофим",
"ТумаNN",
"Тумар & Зарина",
"Турал Тагиев",
"Турбо",
"Турбомода",
"Турбомода feat. Alfa-X",
"Туссин Плюс & Chipachip",
"Тутси",
"Тушкан",
"ТЧБК feat. Леша Свик",
"Тынис Мяги",
"Тяни-Толкай",
]

litera = SoundSymbol.objects.get(name="Т")

count = 0

for tag in т_rus_list_2:
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

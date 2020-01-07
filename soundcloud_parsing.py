
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

о_rus_list_1 = [
"О бедном гусаре замолвите слово",
"О'Ни",
"Оutline Cтудия",
"Обжигающие",
"Обратите Внимание",
"Обратная Сторона",
"Обыкновенное чудо",
"Овсиенко Татьяна",
"Оганезов, Варин, Вишневский",
"Однажды",
"Одни На Двоих",
"Ойра! feat. Юлия Коган",
"Океан Ельзи",
"Океан Эльзы",
"Окиана",
"Оксана Kraski",
"Оксана Бархат",
"Оксана Билера и Настасия",
"Оксана Бойко",
"Оксана Володина",
"Оксана Джелиева",
"Оксана Довгань",
"Оксана Иванова",
"Оксана Казакова",
"Оксана Ковалевскаяt",
"Оксана Ленская",
"Оксана Мазоха",
"Оксана Орлова (Башинская)",
"Оксана Почепа",
"Оксана Симон",
"Оксана Фёдорова",
"Оксана Юхрина",
"Октава",
"Олег Альпийский",
"Олег Алябин",
"Олег Андрианов",
"Олег Белгородский и группа ША",
"Олег Белый (Шевченко)",
"Олег Борисов",
"Олег Булацкий и Ирина Нельсон",
"Олег Бухарцев",
"Олег Варварюк",
"Олег Верд",
"Олег Винник",
"Олег Владимиров",
"Олег Газманов",
"Олег Гетманский",
"Олег Голубев",
"Олег Гонтарь",
"Олег Горте",
"Олег Горшков",
"Олег Груз",
"Олег Ефремов",
"Олег Изотов feat. Лок Дог & Анна Микульская",
"Олег Кай",
"Олег Карпович",
"Олег Кваша",
"Олег Кензов",
"Олег Коренюгин",
"Олег Кричевский",
"Олег Лифановский",
"Олег Лихачев",
"Олег Ломовой",
"Олег Лукьянчук",
"Олег Майами",
"Олег Митяев",
"Олег Муренко",
"Олег Палкин",
"Олег Пахомов",
"Олег Петелин",
"Олег Погудин",
"Олег Пониматко",
"Олег Попков",
"Олег Протасов",
"Олег Сапегин",]

о_rus_list_2 = [
"Олег Сидоров",
"Олег Скобля",
"Олег Смит",
"Олег Снегов",
"Олег Тищенко",
"Олег Фадеев",
"Олег Филатов",
"Олег Хромов",
"Олег Чубыкин",
"Олег Шак",
"Олег Шаумаров",
"Олег Яковлев",
"Олег Янченко",
"Олейник",
"Олександр Войтко",
"Олександр Онофрійчук і Денис Шинкевич",
"Олександр Пономарьов",
"Олександр Порядинський",
"Олесь Богус",
"Олеся Астапова",
"Олеся Атланова",
"Олеся Евстигнеева",
"Олеся Орешёнкова",
"Олеся Павлова",
"Олеся Рублёва",
"Олеся Слукина",
"Оливер Другой",
"Ольга Lee",
"Ольга Алмазова и Михаил Барский",
"Ольга Арефьева",
"Ольга Афанасьева",
"Ольга Баскаева",
"Ольга Бузова",
"Ольга Василюк",
"Ольга Вишня",
"Ольга Вольная",
"Ольга Вронская",
"Ольга Горбачева",
"Ольга Дорофеева (Milissa)",
"Ольга Задонская",
"Ольга Зарубина",
"Ольга и Тимур Ментесашвили",
"Ольга Канайкина",
"Ольга Климентьева",
"Ольга Кляйн",
"Ольга Комарова",
"Ольга Кормухина",
"Ольга Кочеткова",
"Ольга Лима",
"Ольга Литвиненко",
"Ольга Лозина",
"Ольга Майорова",
"Ольга Маковецкая",
"Ольга Мызникова",
"Ольга Наумова",
"Ольга Оболенская",
"Ольга Орлова",
"Ольга Павенская",
"Ольга Пирагс",
"Ольга Плотникова",
"Ольга Полякова",
"Ольга Пульга",
"Ольга Ракицкая",
"Ольга Рогожникова",
"Ольга Романовская",
"Ольга Роса",
"Ольга Семёнова",
"Ольга Сергеева",
"Ольга Серябкина",
"Ольга Соколова",
"Ольга Стельмах",
"Ольга Стронадко",
"Ольга Фаворская",
"Ольга Чистякова",
"Ольга Шестакова",]

о_rus_list_3 = [
"Ольга Щёголь",
"Оля Баскаева",
"Оля Вольная",
"Оля Грэм feat. Lexxus & Milissa",
"Оля Краснова",
"Оля Ла Ева",
"Оля Полякова",
"Оля Ракицкая и #Мойгород",
"Оля Цибульская",
"Омар Хамза",
"Операция Пластилин",
"Орбита и Слава Шанс",
"Оркестр Кинематографии П.У. М. Эрмлера",
"Орская Маргарита",
"Оскар Кучера",
"Ост feat. PaulBlack",
"ОТиДО",
"Отпетые Мошенники",
"Отто Нотман",
"Оу74",
"ОченьКрасивые (ОК)",
]

litera = SoundSymbol.objects.get(name="О")

count = 0

for tag in о_rus_list_3:
    tracks = client.get('/tracks', q=tag, limit=page_size, linked_partitioning=1)
    if tracks:
        for track in tracks.collection:
            created_at = track.created_at
            created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
            try:
                SoundParsing.objects.get(id=track.id)
            except:
                if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                    try:
                        self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                    except:
                        self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                    genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                    new_track = SoundParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, stream_url=track.stream_url, title=track.title, uri=track.uri, release_year=track.release_year)
                count = count + 1
        while tracks.next_href != None and count < 2000:
            tracks = client.get(tracks.next_href, limit=page_size, linked_partitioning=1)
            for track in tracks.collection:
                created_at = track.created_at
                created_at = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                try:
                    SoundParsing.objects.get(id=track.id)
                except:
                    if track.genre and track.release_year and track.duration > 90000 and track.genre in genres_list_names:
                        try:
                            self_tag = SoundTags.objects.get(name=tag, symbol=litera)
                        except:
                            self_tag = SoundTags.objects.create(name=tag, symbol=litera)
                        genre =SoundGenres.objects.get(name=track.genre.replace("'", '') )
                        new_track = SoundParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, duration=track.duration, genre=genre, stream_url=track.stream_url, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

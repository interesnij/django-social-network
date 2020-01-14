
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

р_rus_list_1 = [
"Р.О.М.А.",
"Ра-Мир",
"Рада Рай",
"Ради славы",
"Радио Точка",
"Радиоволна",
"Радион & T1One",
"Радиопомехи",
"Радиофреш",
"Радистка Кэт",
"Радмир Руф feat. Дима Карташов",
"Радмир Текеев",
"Радослава",
"Радуга",
"Радуница",
"Размер project",
"Раим Тригер",
"Раиса Неменова",
"Раиса Отрадная",
"Рай Рада",
"Райво",
"Раймер feat. H1GH & Oks",
"РАЙми",
"Район Моей Мечты",
"Ракета",
"Ракетобиль",
"Ральф и Лилас",
"Рамиль Габитов",
"Рамин Абдулаев",
"Ранетки",
"Ранфил",
"Рапсат",
"Рапунцель",
"Раскольников feat. Саша Отягчающий",
"Расти feat. Келебро",
"Рауш",
"Рафаэль",
"Рафил Минаев",
"Рахманинов",
"Рашель",
"Рашид Ягияев",
"Рашида",
"Реакция",
"Регина Тодоренко",
"Редкая Птица",
"Рекард",
"Рекард feat. Джиос",
"РекиРечи",
"Рем Дигга",
"Ренат Джамилов",
"Ренат Патахов",
"Рената & Диана Индиана",
"Рената Штифель",
"Реновация",
"Ресепшен",
"Респект",
"Республика",
"Ресторатор & Tyomcha K.",
"Рефат Мустафаев",
"Ри (Ri)",
"Ри-Анна",
"Ризван Алиев",
"Ризван Юсупов",
"Рималд",
"Римский-Корсаков",
"Рина СВОЯ feat. Bizaro",
"Ринат Каримов",
"Ринат Сафин",
"Рита Дакота",
"Рита Че",
"Ритм Дорог",
"Рифат Авазов",
"Рихард Вагнер",
"Риша Марк",
"Ришат Сафин (Rishat)",]

р_rus_list_2 = [
"Ріплей",
"Роберт Каракетов",
"Роберт Оганян",
"Робин Гуд",
"Родион Варежкин и Алексей Романюта",
"Родион Газманов",
"Родион Толочкин",
"Родники",
"Рождество",
"Роза Герц",
"Роза Мажонц",
"Розенбаум",
"Рок-Острова",
"Роксана Бабаян",
"Рома kraSh",
"Рома Акустик",
"Рома Белов",
"Рома Бисеров",
"Рома В.П.Р.",
"Рома Дождь",
"Рома Жёлудь",
"Рома Жуков",
"Рома Заря",
"Рома Зверь & Лампочка",
"Рома Идиятуллин",
"Рома Крот feat. ExD",
"Рома Лукин",
"Рома Медведев",
"Рома Пуля",
"Рома Риччи",
"Рома Риччи & DJ Arhipoff",
"Рома Рэй",
"Рома Рязанский",
"Рома Суровый & Isla de Muerta",
"Рома Темный feat. Einer",
"Рома Штайн",
"Ромади",
"Роман Bestseller",
"Роман Архипов",
"Роман Богачев",
"Роман Ващук",
"Роман Гайдмн",
"Роман Гапонов",
"Роман Дистайлов & D.Po",
"Роман Зомби feat. Ай-Q",
"Роман Исаев & Kurganskiy",
"Роман Июльнов",
"Роман Костыренко",
"Роман Левобережный",
"Роман Мануйлов",
"Роман Матюшин",
"Роман Огнев",
"Роман Полонский",
"Роман Пызгорев",
"Роман Рыбин",
"Роман Рябцев",
"Ромарио feat. Женя Любич",
"Ромашка и Монашка",
"Ромео Должен Умереть",
"Рондо",
"Роника",
"Рослана и Батон",
"Россияне",
"Ростислав Галаган",
"Ростислав Поспелов",
"Ротару София",
"Рояль Вио",
"Рубака feat. Дым (Легенды Про)",
"Руки Вверх",
"Рукола",
"Русалочка",
"Руслан PRO-X feat. КириLL",
"Руслан Абкадиров",
"Руслан Агоев",
"Руслан Алехно",]

р_rus_list_3 = [
"Руслан Арыкпаев",
"Руслан Богачев",
"Руслан Гармов",
"Руслан Гасанов",
"Руслан Грабовий",
"Руслан Гюрджян",
"Руслан Дьяков",
"Руслан Исаков",
"Руслан Кайтмесов и Айнара",
"Руслан Квак",
"Руслан Костов",
"Руслан Кримлидис feat. Diazz",
"Руслан Лукаа",
"Руслан Марченко",
"Руслан Масюков",
"Руслан Муратов",
"Руслан Навроцкий",
"Руслан Рино",
"Руслан Уфимский",
"Руслан Хибиртов",
"Руслан Шанов",
"Руслана Собиева",
"Руслана та Олександр Ксенофонтов",
"Русская песня",
"Русские Ди-Джеи",
"Русский Размер",
"Русский Стилль",
"Руставели",
"Рустам Анхель",
"Рустам Бадалов",
"Рустам Джихаев",
"Рустем Жига",
"Рыбачёв и Рыбка",
"Рыночные Отношения",
"Рэджл (Rejl)",
"РЭЙ (RAY)",
"Рэпанутые",
"Ряженка",
"Рязанский Хор Е. Попова",
]

litera = SoundSymbol.objects.get(name="Р")

count = 0

for tag in р_rus_list_3:
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

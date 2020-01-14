
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

и_rus_list_1 = [
"И-Смаил feat. Яна Башкирева",
"И. Николаев и Руки вверх",
"Иlю",
"Ибрагим Ильясов",
"ИВ",
"Иван Банников",
"Иван Васильевич меняет профессию",
"Иван Ганзера",
"Иван Жуков",
"Иван Ильичёв",
"Иван Картышев",
"Иван Козловский",
"Иван Кофф",
"Иван Купала",
"Иван Кучин",
"Иван Нечаев",
"Иван Поклонский",
"Иван Рейс feat. Stinie Whizz",
"Иван Розин (Gouache)",
"Иван Сид",
"Иван Смелик",
"Иван Солопчук",
"Иван Таирян",
"Иван Тетенов",
"Иван Федоренко и Анита Цой",
"Иван Фокин & Диана Валеева",
"Иванна",
"Иванов Александр & Елена Третьякова",
"Иванушки International",
"Иваси",
"Иверия",
"Ига",
"Игорёк",
"Игорёк и Гульназ",
"Игорь Meys",
"Игорь noD",
"Игорь Pumphonia ( N.W.O.B.)",
"Игорь Z-Kay",
"Игорь Ашуров",
"Игорь Барабаш",
"Игорь Бондаренко",
"Игорь Браславский",
"Игорь Бутман",
"Игорь Бучин",
"Игорь Виданов",
"Игорь Герц",
"Игорь Головко",
"Игорь Голубев",
"Игорь Горный",
"Игорь Дань",
"Игорь Демарин",
"Игорь Десятников",
"Игорь Добролевский",
"Игорь Дрягилев",
"Игорь Дубов",
"Игорь Ефименко",
"Игорь Закружных",
"Игорь Иванов",
"Игорь Кваша",
"Игорь Кибирев",
"Игорь Колюха",
"Игорь Корнелюк",
"Игорь Корнилов",
"Игорь Костюхин",
"Игорь Кочконян",
"Игорь Крутой",
"Игорь Крылов",
"Игорь Латышко",
"Игорь Лейс",
"Игорь Луканюк",
"Игорь Манахов",
"Игорь Марков",
"Игорь Махачкалинский",
"Игорь Муромский",
"Игорь Наджиев",]

и_rus_list_2 = [
"Игорь Николаев",
"Игорь Огурцов",
"Игорь Пиджаков",
"Игорь Прэйс",
"Игорь Прэйс feat. Катя Прэйс",
"Игорь Савченко",
"Игорь Сапыцкий",
"Игорь Сахалин",
"Игорь Скляр",
"Игорь Слуцкий",
"Игорь Тальков",
"Игорь Татаренко",
"Игорь Таушканов и Мария Азарская",
"Игорь Тузов",
"Игорь Туринский",
"Игорь Тухватов и Вячеслав Самарин",
"Игорь Шаров",
"Игорь Шелудько",
"Игорь Щедров и Сергей Мироненко",
"Игорь Ященко",
"Игра Слов",
"Игрушки",
"Ида Квагинидзе",
"Идефикс",
"Изабелла Юрьева",
"Изгоняющий дьявола",
"Изгоняющий Дьявола 2: Еретик",
"Измена",
"Изольда",
"Ика",
"Илага",
"Илия & Анжела Видяпина",
"Илона Кесаева",
"Ильдар Южный",
"Ильшат",
"Илья Daff & Костя Сайб",
"Илья Krosssy",
"Илья MZT",
"Илья Privat",
"Илья Romeo",
"Илья VerTigo feat. Markiza",
"Илья Белау",
"Илья Гуров",
"Илья Гусев",
"Илья Жилкин",
"Илья Зудин",
"Илья Киреев",
"Илья Лагутенко",
"Илья Лукин",
"Илья Маградзе",
"Илья Н",
"Илья Орлов",
"Илья Пладо",
"Илья Подстрелов",
"Илья Ривман",
"Илья Руди",
"Илья Таланов",
"Илья Темнов feat. Jimmie Naif",
"Илья Фишерман",
"Илья Чужой",
"Илья Щербаков",
"Илья Юдичев",
"Илья Яббаров",
"Ильяна и Dj Slon",
"Илюха Lv",
"Импай",
"Импай feat. Lexana",
"Империя",
"Имя Фамилия",
"Инвойс",
"Инга Гай",
"Индаблэк",
"Индиго",
"Индиго feat. Сацура",
"Индустрия Снов",]

и_rus_list_3 = [
"Инесса Михно",
"Инна Вальтер",
"Инна Воронова",
"Инна Годунова",
"Инна Желанная",
"Инна Лайф",
"Инна Литвин",
"Инна Маликова",
"Инна Новикова",
"Инна Субботина",
"Инна Тимофеева & Саша Тверье",
"Инна Улановская",
"Иной feat. Хава",
"Инсайт Project",
"Инстинкт",
"Интарс Бусулис",
"Интонация (In2Nation)",
"Интуиция",
"Инфинити",
"Инь-Ян",
"Иоганн Штраус",
"Иоганнес Брамс",
"Ион Суручану",
"Ионна Алекс",
"Иосиф Кобзон",
"Ира PSP",
"Ира Левицкая",
"Ира Софьянова",
"Ира Темичева",
"Ира Тонева",
"Иракли",
"Ираклий",
"Ирида",
"Ирина Cherry Черкасова",
"Ирина Алегрова",
"Ирина Алишихова",
"Ирина Аллегрова",
"Ирина Архангельская",
"Ирина Баженова",
"Ирина Билык",
"Ирина Блохина",
"Ирина Богушевская",
"Ирина Видова",
"Ирина Влади",
"Ирина Гвоздева",
"Ирина Глебова",
"Ирина Дубцова",
"Ирина Дюкова",
"Ирина Евсюкова feat. Kusenov & SerezhaDesss",
"Ирина Желнова",
"Ирина Камянчук",
"Ирина Каспер",
"Ирина Коган",
"Ирина Круг",
"Ирина Кузнецова",
"Ирина Кулькова",
"Ирина Левандовская",
"Ирина Май",
"Ирина Максимова",
"Ирина Меньшенина",
"Ирина Мирошниченко",
"Ирина Муравьева",
"Ирина Нельсон",
"Ирина Омель & Nikas",
"Ирина Ортман",
"Ирина Понаровская",
"Ирина Прима",
"Ирина Рибейро",
"Ирина Желнова",
"Ирина Камянчук",
"Ирина Каспер",
"Ирина Коган",
"Ирина Коган и Мафик",
"Ирина Круг",
"Ирина Круг и Edgar",
"Ирина Круг и Алексей Брянцев",
"Ирина Кузнецова",
"Ирина Кулькова",
"Ирина Кулькова и Дмитрий Нестеров",
"Ирина Левандовская",]

и_rus_list_4 = [
"Ирина Май",
"Ирина Максимова",
"Ирина Меньшенина",
"Ирина Мирошниченко",
"Ирина Муравьева",
"Ирина Нельсон",
"Ирина Нельсон и Денис Клявер",
"Ирина Нельсон, Димитрий Колдун, Денис Клявер, Юлия Михальчик",
"Ирина Омель & Nikas",
"Ирина Ортман",
"Ирина Ортман feat. DJM Гребенщиков",
"Ирина Ортман feat. Александр Киреев",
"Ирина Ортман feat. Всё Включено",
"Ирина Понаровская",
"Ирина Прима",
"Ирина Рибейро",
"Ирина Ру",
"Ирина Рысь",
"Ирина Салтыкова",
"Ирина Сун",
"Ирина Туманова",
"Ирина Федоруца",
"Ирина Цуканова",
"Ирина Шведова",
"Ирина Широкова",
"Ирина Шотт",
"Ирина Эмирова",
"Иркутский",
"Ирма Брикк",
"Ирма Нойман",
"Ирсон & Nikita Malinin",
"Ирсон Кудикова",
"Исаак Дунаевский",
"ИСАЙЯ",
"Искра",
"Ислам и Карина Киш",
"Ислам Итляшев",
"Исми",
"История Игрушек 3",
"Ищу Продюсера",
"Июль",
"Ияра",

]
litera = SoundSymbol.objects.get(name="И")

count = 0

for tag in и_rus_list_4:
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

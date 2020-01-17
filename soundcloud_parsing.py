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

z_rus_list_1 = [
"Z Dimention feat. Lady Drum",
"Z feat. Fetty Wap",
"Z-People",
"Z-Ro feat. Rick Ross",
"Z.A.R.B & NiFTO feat. Kelis",
"Za-Mir",
"Za.U.R. & DJ Varda",
"Zaa feat. Molly Bancroft",
"ZAA Sanja Vucic",
"Zaac",
"Zabava",
"Zabot feat. Caelu",
"Zac Brown Band feat. Sara Bareilles",
"Zac Efron & Zendaya",
"Zac Samuel",
"Zac Waters",
"Zac Waters & Victor",
"Zach Berkman",
"Zach Teiser feat. Erin Levins",
"Zachary Zamarripa",
"Zack Hamsey",
"Zack Knight",
"Zack Martino",
"Zack Mia",
"Zack Shaar",
"Zadar",
"ZadeKing",
"ZADI",
"Zaeden",
"Zagaza feat. Jay Millar, J X & Drei Ros",
"Zage feat. Ekatherina April",
"Zagray",
"Zaho",
"Zahozhiy",
"Zaia",
"Zaira feat. EL 3Mendo",
"Zak Abel",
"Zak Waters",
"Zakkov feat. Nathan Brumley",
"Zala Kralj & Gasper Santl",
"Zambezi",
"Zameer",
"Zander Bleck",
"Zane Williams",
"ZangieV feat. Peppa",
"Zanski feat. Bombs & Bottles",
"Zapp",
"Zara feat. Jorge Nava",
"Zara feat. Snatt & Vix",
"Zara Kershaw",]

z_rus_list_2 = [
"Zara Larsson",
"Zarcort feat. Ambar Garces & Piter-G",
"Zardi",
"Zardonic",
"Zarga",
"ZaRiNa",
"Zarkana",
"Zarubin & Bystrov",
"Zary feat. Rhea Raj",
"Zatonsky Feat. Ange",
"Zave feat. Mayowa",
"Zayn",
"Zayn Malik",
"ZAZ",
"Zazen",
"Zazoo",
"Zdob Si Zdub",
"Ze Mike feat. Саша Маст",
"Zealyn",
"Zebra",
"Zebrahead feat. Jean Ken Johnny",
"ZeBros Band",
"Zecko feat. Isac Torres",
"Zed Bias & Stylo G",
"ZedBazi feat. Behzad Leito",
"Zedd",
"Zedd, Matthew Koma, Miriam Bryant & R3hab",
"Zedef & Treeko",
"Zeds Dead",
"Zedsky",
"Zeeba",
"Zeen",
"Zefanio feat. Josylvio",
"Zein",
"ZeinaLove",
"Zeke Thomas",
"Zekiel",
"Zeleno",
"Zelish",
"Zeljko Joksimovic",
"Zelkin",
"Zell & Nard",
"Zell Hanssen",
"Zella Day",
"Zelll feat. Marck",
"Zen Freeman",
"Zen Garden Deejays feat. Joseph Mills",
"ZenAware feat. Suriel Hess",
"Zenbi Ft. Rachael Starr",
"Zendaya",]

z_rus_list_3 = [
"Zeni N",
"Zennus",
"Zeno",
"Zenttric",
"Zeper & Delove feat. Rachel Woznow",
"Zerb",
"Zero 7",
"Zerotic & Tiger Twiist",
"Zeskullz",
"Zetandel",
"Zeus Faber",
"Zhala",
"Zhanna Davtyan",
"Zhannett Saparova",
"Zhao, Felix, Ray Jamsrock",
"Zhavia Ward",
"Zhi-vago",
"ZHIKO & Antoine Cara",
"Zhila feat. Влад KesH & Витя Сенс",
"ZHR feat. Amiram Eini",
"ZHU",
"ZiBBZ",
"Ziggy & Syzz",
"Ziggy Marley",
"Zigzag",
"ZiK feat. Pas & Паша Мэд",
"Zikai",
"Zimmer",
"Zimpzon & Braak",
"Zina",
"Zinner",
"Zion & Lennox",
"Zip92",
"ZippO",
"Zir Rool",
"ZIROY",
"Zirra feat. Santi",
"Zita feat. Ben Woodward & Coopa",
"Zivert",
"Zizzo feat. Jay Di",
"ZK & TRUEтень",
"Zkmn feat. RE-pac",
"Zkrmn",
"Zlata (Злата)",
"Zlatan Ibrahimovic feat. Day",
"ZLN",
"ZlyD & Люфт",
"Zmily",
"Znaki",
"Zoe",]

z_rus_list_4 = [
"Zoe Badwi",
"Zoe Nash",
"Zola Jesus",
"Zoli Adok",
"Zoli Vekony & Michelle Lewin feat. Yinka Williams",
"Zoloto",
"Zolotoy",
"Zoma",
"Zombic",
"Zombie Cats",
"Zombie Killers",
"Zomboy",
"Zomby Girlz",
"Zonatto & Bruno Motta feat. Ebo Live",
"Zonderling",
"Zonnique",
"Zoo Brazil",
"Zoo Reality",
"Zookeepers",
"Zookeper",
"Zoopreme feat. Krysta Youngs & Julia Ross",
"Zoot Woman feat. Kylie Minogue",
"Zoozee",
"Zowie",
"Zoya",
"ZROQ & Cris Hagman",
"Zsak",
"Zsombee",
"Zsombor K & Mr Andre",
"ZSUN feat. BM",
"Zucchero",
"Zucchi & Wadd feat. DreCoy",
"Zuda",
"Zuka",
"Zulfiya Gadzhieva & Gidayyat",
"Zuma & Kosta feat. MC Shayon",
"Zumii feat. Kyla",
"Zvaga feat. Crest'One",
"Zvensky",
"Zventa Sventana",
"Zveroboy",
"Zvezda",
"Zvika Brand",
"ZVUK",
"Zvuki",
"Zwette feat. Molly",
"ZWUAGA",
"Zwuaga & Maisa",
"Zxna",
"Zyomka",
"Zyon",
"ZZ Top",
"ZZ Ward",
"Zzabelin",
"Zабава",
"Zавтра",
"Zоряна",
]

litera = SoundSymbol.objects.get(name="Z")

count = 0

for tag in z_rus_list_1:
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
                    new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
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
                        new_track = SoundcloudParsing.objects.create(id=track.id, tag=self_tag, artwork_url=track.artwork_url, created_at=created_at, description=description, duration=track.duration, genre=genre, title=track.title, uri=track.uri, release_year=track.release_year)
                    count = count + 1

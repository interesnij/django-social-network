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

y_rus_list_1 = [
"Y-US",
"Y.A.S",
"Y.V.E. 48",
"Y2K",
"Ya Rick feat. Skochy",
"Ya-Ya",
"Yaar feat. Kanita",
"Yabee",
"Yaboimatoi",
"Yacku feat. Aneesa",
"Yada26 feat. Shami",
"Yaeger",
"Yaeji",
"Yael Naim",
"Yahel",
"Yakarta & Srta. Dayana",
"Yaki-Da",
"Yakimova Di",
"Yakubovski",
"YalaV",
"Yalin",
"Yall",
"Yalu",
"Yam Nor",
"Yama",
"Yamada feat. Elle Vee",
"Yamira",
"Yamppier feat. Fillo",
"Yamych",
"Yamzy",
"Yan Kings & Matt Petrone feat. Pitbull",
"Yan Oxygen",
"Yan Space",
"Yan Veter",
"Yana Beliz",
"Yana En Fly",
"Yana Kay",
"YanaKlim",
"Yandel",
"Yaneena",
"Yang & Cari",
"Yang Feat. Amy Kirkpatrick",
"Yanger",
"Yanik Coen & Richard Beynon",
"Yanis.S feat. Logan Milan",
"Yanitsa & Arti",
"Yanix",
"Yankie & Jeian",
"Yann Muller",
"Yann Tiersen",]

y_rus_list_2 = [
"Yanni",
"Yanni Hrisomallis",
"Yannick Fuchs",
"Yano Project & Sismica",
"Yanou feat. Andreas Johnson",
"Yanou feat. Falco Luneau",
"Yantra Mantra",
"YARI A",
"Yariko",
"Yaro",
"YarosLOVE",
"Yas Cepeda feat. Ella",
"Yash & Sanders",
"Yash Narvekar & Akasa",
"Yasirah",
"Yasmeen & Danism",
"Yasmin feat. Shy FX & Ms Dynamite",
"Yasmin Green",
"YASUCA",
"Yasuharu Takanashi",
"Yasutaka Nakata feat. Charli XCX & Kyary Pamyu Pamyu",
"Yates",
"Yatharth",
"Yaya",
"Yaz feat. Lstnyt",
"Yazoo",
"YBN Nahmir feat. City Girls & Tyga",
"Ye Ali feat. K Camp",
"Yeah Yeah Yeahs",
"Years",
"Yegor Gray",
"Yelaman & Ирина Кайратовна",
"Yelawolf",
"Yella Beezy",
"Yelle",
"YellLow",
"Yello",
"Yellow Claw",
"Yellow Days",
"Yellow Hills",
"Yellow Monkeys Team",
"Yellowcard",
"Yellowman",
"Yenn & Halev",
"Yepha",
"Yera & Mau Y Ricky",
"Yera & Morat",
"Yeriel",
"Yes-R",
"YesYou feat. Michael Marshall",]

y_rus_list_3 = [
"Yeyo",
"YG",
"Yianna Terzi",
"Yiddu Delhi",
"Yigit Unal",
"Ying Yang Twins feat. Greg Tecoz",
"Yinon Yahel",
"Yira",
"Yiruma",
"Yk Osiris feat. Tory Lanez & Ty Dolla Sign",
"YLA",
"Ylande",
"Yletai",
"Ylona",
"Ylva",
"Ylvis",
"YNGA feat. Brianna",
"Yngwie Malmsteen",
"Yo Gotti",
"Yo La Tengo",
"Yoana",
"Yoandri",
"Yoav",
"Yodis feat. Christina Maria",
"Yoel Lewis",
"Yogi",
"Yohio",
"Yoji Biomehanika",
"Yoko Takahashi",
"Yolan & Kenia",
"Yolanda Be Cool",
"Yolanda Selini feat. Dreamon",
"Yolla",
"YONAKA",
"Yonas",
"Yoni Jay",
"Yoni Teran",
"Yonna",
"Yonta",
"YOOKiE & Hekler",
"YorGa feat. Brighi",
"York",
"Yorke",
"Yoshiki, Hideo Hirata & Yoshiki Studio Orchestra",
"Yotuel",
"You In Mind",
"You Me At Six",
"You Raise Me Up",
"You-Ra",
"You+Me",]

y_rus_list_4 = [
"Young Ash & Kg Man vs. Claydee",
"Young Bombs",
"Young Boss",
"Young Buck",
"Young Cash feat. Akon",
"Young Chris",
"Young De Aka Demrick",
"Young Deenay",
"Young Empires",
"Young Fame feat. Бьянка",
"Young Fathers",
"Young Franco",
"Young Gipsy feat. Young Monte Mono",
"Young Goga",
"Young Greatness feat. Akon",
"Young Guns",
"Young Jeezy",
"Young Johnson & Tony Tonite",
"Young Karin",
"Young Killer",
"Young London",
"Young Money feat. Nicki Minaj",
"Young Obama & Javvani",
"Young P&H",
"Young Rising Sons",
"Young Squage feat. Stockholm Syndrome",
"Young Swift feat. Akon",
"Young T & Bugsey",
"Young The Giant",
"Young Thug",
"Young Wolf Hatchlings",
"YoungBoy Never Broke Again",
"Youngman",
"Youngr",
"Younha feat. RM",
"YouNotUs",
"Your Smith",
"Youssou N'Dour",
"Youth",
"Youth Lagoon",
"Youthonix feat. Arrow Benjamin",
"Yowda feat. Riff Raff",
"Yozo feat. Bonnie Legion",
"Ypey",
"Ysa Ferrer",
"Yssa",
"YT Triz feat. Rick Ross & Lil Wayne",
"Yuen Perez",
"Yuga feat. Candi Staton",
"Yuhki Kuramoto",]

y_rus_list_5 = [
"Yuichi Watanabe",
"Yuka Port",
"Yuki Murata",
"Yuko",
"Yuksek Sadakat",
"Yulara",
"Yulee",
"Yulez",
"Yulia Verkh",
"Yulien Oviedo feat. Gente De Zona",
"Yulis Feat. Alex Maxim",
"Yuliya Rybakova",
"Yuliyou",
"Yumi Zouma",
"Yuna",
"Yunberg",
"Yunel, Ne-Yo & J. Alvarez",
"Yung 'n Usls",
"Yung Berg",
"Yung Gravy feat. Juicy J",
"Yung Joc feat. T-Pain",
"Yung Pinch & GASHI",
"Yung Pretender feat. Chilli Chilton",
"Yung Trappa",
"Yung Zotik",
"Yungblud",
"Yungen",
"Yuno",
"Yunus Durali",
"Yuoff",
"Yuranis Leon & DJ Dever & Mr Black El Presidente",
"Yurban",
"Yurena",
"Yuri Kane",
"Yuri Samarkin",
"Yuridia",
"Yuriko Nakamura",
"Yurima",
"Yuriy Berliny",
"Yuriy Poleg & Phillipo Blake ft. V.Ray",
"Yus",
"Yusef Lateef",
"Yusuf OZER",
"Yvan & Callendula",
"Yve feat. Bissiko",
"Yves Larock",
"Yves Murasca & Ron Carroll",
"Yves V",
"Yves Vandewalle",
"Yvette Horner",
"YVR",
"Yvvan Back",
]

litera = SoundSymbol.objects.get(name="Y")

count = 0

for tag in y_rus_list_5:
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

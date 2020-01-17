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

u_rus_list_1 = [
"U So Witty",
"U-GiN",
"U-Phoria",
"U-Th",
"U.D.O.",
"U.K.",
"U.M.Project",
"U137",
"U2",
"U3U",
"U4",
"U96",
"Uachik",
"Ub 40",
"UB40",
"Uber",
"Uberjak'd",
"UBI feat. TomE & Rime",
"Uche",
"Uche feat. Martin Silence",
"Udalin Project",
"Udbet",
"Udc",
"Uddi",
"Udex",
"UDM",
"Ufo Project",
"Ufo361 feat. Data Luv",
"Uforik feat. MZ",
"Ufuk Sakizcioglu feat. Burcu",
"Ugly Duckling",
"UGLYAROV",
"Ugress",
"Ugroza project",
"Ugur Can Yenal feat. Gunes Taskiran",
"UhreWaja",
"Uknow",
"ULA",
"Uli Jon Roth",
"Ulika",
"Ulka vs. DJ Max Myers & Rifatello",
"Ulker",
"Ulrich Schnauss",
"Ulrika",
"Ultimate",
"ultr@звук",
"Ultra Girls",
"Ultra Nate",
"Ultra Ultra",
"Ultra-Sonic",]

u_rus_list_2 = [
"UltraHype",
"ULTRAMARIN",
"Ultrasyd",
"Ultraviolence",
"Ultraviolet Sound",
"Ulukmanapo feat. DJ Feray",
"Ulver",
"Uma2rman",
"Umbrella (ex. Vendetta)",
"Umbrella (Vendetta)",
"Umbrella MC",
"UMEK",
"Ummet Ozcan",
"Umpire feat. Liz Kretschmer",
"Umut Dogan",
"Umut Kilic",
"Una Sand",
"Unc feat. Viky Red",
"UNC vs Dirty Nano",
"Uncle B.",
"Uncle Kracker",
"Unclesand",
"Under This",
"UnderCover",
"Underdog Project",
"Underlow",
"Undr",
"Undressd",
"Uness",
"Unge Ferrari feat. Medina",
"Unicq",
"Unidentified",
"Union J",
"Unique",
"Unis Abdullaev",
"Unisong",
"Unisonic",
"United Family",
"United States Of Dance",
"Uniting Nations",
"Unity Loops",
"Universal Project",
"Universal Sense",
"Universe",
"Univz",
"UNKLE",
"Unklfnkl",
"Unknown",
"Unlike Pluto",
"UnoMas & Dave Sol",]

u_rus_list_3 = [
"UnorthodoxX vs. Zolotoy",
"Unree",
"Unrest",
"Untitled Basement Chiller",
"Untitled feat. Ludacris",
"Untone Chernov",
"UOMO",
"Up 'n' Dance",
"Upjeet",
"Uplink ",
"Uppermost",
"UpsideDown feat. Jaz Dhami",
"Uptown Funk Empire",
"Urba Y Rome feat. Lyanno & Zion & Lennox",
"Urban Chill",
"Urban Cone",
"Urban Contact",
"Urban Cookie Collective",
"Urban Dance Crew",
"Urban Love",
"Urban Phunk Society",
"Urban Symphony",
"Urban Trad",
"Urbandawn feat. Thomas Oliver",
"Urbanstep feat. Micah Martin",
"URBN",
"Urge Overkill",
"Uriah Heep",
"Ursine Vulpine feat. Annaca",
"Urthboy feat. Tiaan",
"US",
"Us The Duo",
"USB",
"Usher",
"Ustinova",
"Uto Karem",
"UtroVechera",
"UTS Hybrid Remix",
"Uun",
"Uzari & Maimuna",
"UZOO",
]

litera = SoundSymbol.objects.get(name="U")

count = 0

for tag in u_rus_list_2:
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

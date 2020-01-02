# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
django.setup()

import soundcloud
from music.models import SoundParsing


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
page_size = 200
all_tracks = client.get('/tracks', order='created_at', limit=page_size, linked_partitioning=1)
for track in all_tracks.collection:
    SoundParsing.objects.create(
                                artwork_url=track.artwork_url,
                                bpm=track.bpm,
                                created_at=track.created_at,
                                duration=track.duration,
                                genre=track.genre,
                                permalink=track.permalink,
                                permalink_url=track.permalink_url,
                                release=track.release,
                                release_day=track.release_day,
                                release_month=track.release_month,
                                release_year=track.release_year,
                                stream_url=track.stream_url,
                                streamable=track.streamable,
                                tag_list=track.tag_list,
                                title=track.title,
                                uri=track.uri,
                                isrc=track.isrc,
                                user_name=track.user_name,
                                user_avatar=track.user_avatar,
                                )
while all_tracks.next_href != None and all_tracks.count() < 5001:
    all_tracks = client.get(all_tracks.next_href, order='created_at', limit=page_size, linked_partitioning=1)
    for track in all_tracks.collection:
        SoundParsing.objects.create(
                                    artwork_url=track.artwork_url,
                                    bpm=track.bpm,
                                    created_at=track.created_at,
                                    duration=track.duration,
                                    genre=track.genre,
                                    permalink=track.permalink,
                                    permalink_url=track.permalink_url,
                                    release=track.release,
                                    release_day=track.release_day,
                                    release_month=track.release_month,
                                    release_year=track.release_year,
                                    stream_url=track.stream_url,
                                    streamable=track.streamable,
                                    tag_list=track.tag_list,
                                    title=track.title,
                                    uri=track.uri,
                                    isrc=track.isrc,
                                    user_name=track.user_name,
                                    user_avatar=track.user_avatar,
                                    )

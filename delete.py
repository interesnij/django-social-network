# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from django.conf import settings
from users.models import User
from music.models import SoundList
from video.models import VideoAlbum
from gallery.models import Album

user = User.objects.get(pk=8)

SoundList.objects.create(creator=user, community=None, type=SoundList.MAIN, name="Основной плейлист")
VideoAlbum.objects.create(creator=user, community=None, type=VideoAlbum.MAIN, title="Основной список")

Album.objects.create(creator=user, community=None, type=Album.AVATAR, title="Фото со страницы")
Album.objects.create(creator=user, community=None, type=Album.MAIN, title="Основной альбом")
Album.objects.create(creator=user, community=None, type=Album.WALL, title="Фото со стены")

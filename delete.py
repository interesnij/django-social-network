# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from django.conf import settings
from docs.models import DocList
from music.models import SoundList, Music
from video.models import VideoList
from docs.models import Doc
from chat.models import Message
from gallery.models import PhotoList
from chat.models import Message
from communities.models import Community
from communities.model.settings import CommunityPrivate
import re


text = "Соцсеть трезвый.рус.... строится уже 24 месяцев. Сейчас она в состоянии почти завершенном. Проводятся последние работы, достраиваются нужные разделы (остается режим супер-управленцев, рекламная площадка)."

words = text.split(" ")
if words:
    _loop, _exlude, this, next = [], [], -1, 0
    for word in words:
        print (word)

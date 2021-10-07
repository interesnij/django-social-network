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


text = "Соцсеть трезвый.рус boroda.fm https://street.company строится уже 24 месяцев. Сейчас она в состоянии почти завершенном. Проводятся последние работы, достраиваются нужные разделы (остается режим супер-управленцев, рекламная площадка)."

words = text.split(" ")
if words:
    _loop, _exlude, this, next = [], [], -1, 0
    _loop.append(text)
    for word in words:
        if not word in _exlude and "." in word:
            a = ""
            _loop.append(a)
            this += 1
            next += 1
            if word[-1] in ".,:;!_*-+()/#¤%&)":
                _p = word[:-1]
            else:
                _p = word

            if "трезвый.рус" in _p:
                _loop[next] = _loop[this].replace(_p, '<a onclick="return stop_load_fullscreen(this);" class="ajax underline" href="' + _p + '">' + _p + '</a>')
            else:
                _loop[next] = _loop[this].replace(_p, '<a onclick="return stop_load_fullscreen(this);" class="underline" target="_blank" href="' + _p + '">' + _p + '</a>')
        _exlude.append(word)
    print (_loop[next])

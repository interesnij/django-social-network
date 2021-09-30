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
import re

text = "https://www.youtube.com/1111111 https://www.youtube.com/2222222222 https://www.youtube.com/3333333333"

http = re.findall(r'(https?://[^\s]+)', text)
_loop = []
_loop.append(text)

if http:
    this = -1
    next = 0
    for p in http:
        a = ""
        this += 1
        next += 1
        print ("Ссылка", p)
        print ("=========")
        _loop.append(a)
        if "трезвый.рус" in p:
            _loop[next] = _loop[this].replace(p, '<a class="ajax underline" href="' + p + '">' + p + '</a>')
        else:
            _loop[next] = _loop[this].replace(p, '<a class="underline" target="_blank" href="' + p + '">' + p + '</a>')
        print ("Старая переменная", _loop[this])
        print ("---------")
        print ("Новая переменная", _loop[next])
        print ("---------")

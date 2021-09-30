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

text = "https://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698shttps://www.youtube.com/watch?v=BjwRjaStTGA&t=16698s"

http = re.findall(r'(https?://[^\s]+)', text)
a_1 = text
_loop = [a_1]

if http:
    this = -1
    next = 0
    a = ""
    for p in http:
        this += 1
        next += 1
        _loop.append(a)
        if "трезвый.рус" in p:
            _loop[next] = _loop[this].replace(p, '<a class="ajax underline" href="' + p + '">' + p + '</a>')
        else:
            _loop[next] = _loop[this].replace(p, '<a class="underline" target="_blank" href="' + p + '">' + p + '</a>')
    print (_loop[next])

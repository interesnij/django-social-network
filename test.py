# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from music.models import SoundList
from video.models import VideoList
from posts.models import PostList, Post
from docs.models import DocList
from gallery.models import PhotoList
from survey.models import SurveyList
from goods.models import GoodList
from users.models import User
from users.model.list import *
from communities.models import Community
from communities.model.list import *
from django.db.models import Q
from chat.models import Message

message = Message.objects.get(uuid="1b6bb514-0e6f-47c0-9e33-41164ae9c171")
import re

#print(re.findall(r'data-pk="(?P<pk>\d+)"', message.text))
ids = re.findall(r'data-pk="(?P<pk>\d+)"', message.text)
print(ids)

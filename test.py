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
from posts.models import PostList
from docs.models import DocList
from gallery.models import PhotoList
from survey.models import SurveyList
from goods.models import GoodList

for list in SoundList.objects.all():
    list.update(count=list.count_items())
for list in VideoList.objects.all():
    list.update(count=list.count_items())
for list in PostList.objects.all():
    list.update(count=list.count_items())
for list in DocList.objects.all():
    list.update(count=list.count_items())
for list in PhotoList.objects.all():
    list.update(count=list.count_items())
for list in SurveyList.objects.all():
    list.update(count=list.count_items())
for list in GoodList.objects.all():
    list.update(count=list.count_items())

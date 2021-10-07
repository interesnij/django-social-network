# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

import soundcloud
from music.models import *
from datetime import datetime, date, time
import json, requests
from gallery.models import PhotoList
from goods.models import GoodList
from video.models import VideoList
from music.models import MusicList
from survey.models import SurveyList
from docs.models import DocList

for list in PhotoList.objects.all():
    list.create_el = 7
    list.save(update_fields=["create_el"])
for list in GoodList.objects.all():
    list.create_el = 7
    list.save(update_fields=["create_el"])
for list in VideoList.objects.all():
    list.create_el = 7
    list.save(update_fields=["create_el"])
for list in MusicList.objects.all():
    list.create_el = 7
    list.save(update_fields=["create_el"])
for list in DocsList.objects.all():
    list.create_el = 7
    list.save(update_fields=["create_el"])

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


SoundList.objects.all().update(count=SoundList.count_items())
VideoList.objects.all().update(count=VideoList.count_items())
PostList.objects.all().update(count=PostList.count_items())
DocList.objects.all().update(count=DocList.count_items())
PhotoList.objects.all().update(count=PhotoList.count_items())
SurveyList.objects.all().update(count=SurveyList.count_items())
GoodList.objects.all().update(count=GoodList.count_items())

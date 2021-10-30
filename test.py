
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
from docs.models import DocsList, Doc
from posts.models import PostsList, Post
from communities.models import Community
from communities.model.list import CommunityDocsListPosition
from users.model.list import UserPlayListPosition
from users.models import User


UserPlayListPosition.objects.all().delete()
for u in User.objects.all():
    music_list = MusicList.objects.create(creator=u, type=MusicList.MAIN, name="Основной список")
    UserPlayListPosition.objects.create(user=u.pk, list=music_list.pk, position=1)

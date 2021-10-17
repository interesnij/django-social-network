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
from music.models import SoundList
from survey.models import SurveyList
from docs.models import DocList
from posts.models import PostsList, Post
from users.models import User
from users.model.list import UserPostsListPosition

PostsList.objects.all().delete()
for user in User.objects.all():
    #post_list = PostsList.objects.create(creator=user, type=PostsList.MAIN, name="Записи")
    #post_fix_list = PostsList.objects.create(creator=user, type=PostsList.FIXED, name="Закреплённый список")
    UserPostsListPosition.objects.create(user=user.pk, list=user.get_post_list().pk, position=1)

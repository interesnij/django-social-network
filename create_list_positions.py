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
from users.model.profile import UserProfile
from communities.models import Community
from communities.model.settings import CommunityInfo


post_lists = PostList.objects.all()
for list in post_lists:
    if list.name == "Основной список":
        list.name == "Записи"
        list.save(update_fields=["name"])
    list.count = list.count_items()
    list.save(update_fields=["count"])

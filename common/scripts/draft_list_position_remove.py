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
from posts.models import PostsList, Post
from docs.models import DocList
from gallery.models import PhotoList
from survey.models import SurveyList
from goods.models import GoodList
from users.models import User
from users.model.list import *
from communities.models import Community
from communities.model.list import *
from django.db.models import Q

""" убираем порядки списков постов-предложек, так как они не выведутся шаблоном, хотя надо это в шаблонные скрипты дописать!"""
post_lists = PostsList.objects.filter(type="_DRA")
for list in post_lists:
    try:
        if list.community:
            CommunityPostsListPosition.objects.get(list=list.pk, community=list.community.pk).delete()
        else:
            UserPostsListPosition.objects.get(list=list.pk, user=list.creator.pk).delete()
    except:
        pass

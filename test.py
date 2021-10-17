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
from communities.models import Community
from communities.model.list import CommunityPostsListPosition


CommunityPostsListPosition.objects.all().delete()
for c in Community.objects.all():
    post_list = PostsList.objects.get(creator=c.creator, community=c, type=PostsList.MAIN, name="Записи")
    CommunityPostsListPosition.objects.create(community=c.pk, list=c.get_post_list().pk, position=1)

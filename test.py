
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
from communities.model.list import CommunityPostsListPosition
from users.model.list import UserPlayListPosition
from users.models import User

community = Community.objects.get(pk=1)
post_list = PostsList.objects.create(PostsList.objects.create(creator=community.creator, community=community, type=PostsList.MAIN, name="Записи"):
CommunityPostsListPosition.objects.create(community=community.pk, list=post_list.pk, position=1)

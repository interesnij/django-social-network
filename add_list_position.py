# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from music.models import MusicList
from video.models import VideoList
from posts.models import PostsList, Post
from docs.models import DocsList
from gallery.models import PhotoList
from survey.models import SurveyList
from goods.models import GoodList
from users.models import User
from users.model.list import *
from communities.models import Community
from communities.model.list import *
from django.db.models import Q


for user in User.objects.all():
    if not SurveyList.objects.filter(creator=user, community=None, type=SurveyList.MAIN).exists():
        list = SurveyList.objects.create(creator=user, community=None, type=SurveyList.MAIN)
        UserSurveyListPosition.objects.create(list=list.pk, user=user.pk)

for community in Community.objects.all():
    if not SurveyList.objects.filter(community=community, type=SurveyList.MAIN).exists():
        list = SurveyList.objects.create(creator=community.creator, community=community, type=SurveyList.MAIN)
        CommunitySurveyListPosition.objects.create(list=list.pk, community=community.pk)

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
from users.model.list import *
from communities.models import Community
from communities.model.list import *
from django.db.models import Q


UserPhotoListPosition.objects.all().delete()
UserPostListPosition.objects.all().delete()
UserPlayListPosition.objects.all().delete()
UserGoodListPosition.objects.all().delete()
UserVideoListPosition.objects.all().delete()
UserSurveyListPosition.objects.all().delete()
UserDocListPosition.objects.all().delete()

CommunityPhotoListPosition.objects.all().delete()
CommunityPostListPosition.objects.all().delete()
CommunityPlayListPosition.objects.all().delete()
CommunityGoodListPosition.objects.all().delete()
CommunityVideoListPosition.objects.all().delete()
CommunitySurveyListPosition.objects.all().delete()
CommunityDocListPosition.objects.all().delete()

query = Q(Q(type="PUB")|Q(type="PRI"))

post_lists = PostList.objects.filter(type="_DRA")
for list in post_lists:
    try:
        if list.community:
            CommunityPostListPosition.objects.get(list=list.pk, community=list.community.pk).delete()
        else:
            UserPostListPosition.objects.get(list=list.pk, user=list.creator.pk).delete()
    except:
        pass

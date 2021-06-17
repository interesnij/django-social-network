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

post_lists = PostList.objects.exclude(type="_FIX").exclude(type="_DRA")
for list in post_lists:
    if list.community:
        CommunityPostListPosition.objects.create(list=list.pk, community=list.community.pk)
    else:
        UserPostListPosition.objects.create(list=list.pk, user=list.creator.pk)

doc_lists = DocList.objects.all()
for list in doc_lists:
    if list.community:
        CommunityDocListPosition.objects.create(list=list.pk, community=list.community.pk)
    else:
        UserDocListPosition.objects.create(list=list.pk, user=list.creator.pk)

photo_lists = PhotoList.objects.all()
for list in photo_lists:
    if list.community:
        CommunityPhotoListPosition.objects.create(list=list.pk, community=list.community.pk)
    else:
        UserPhotoListPosition.objects.create(list=list.pk, user=list.creator.pk)

music_lists = SoundList.objects.all()
for list in music_lists:
    if list.community:
        CommunityPlayListPosition.objects.create(list=list.pk, community=list.community.pk)
    else:
        UserPlayListPosition.objects.create(list=list.pk, user=list.creator.pk)

video_lists = VideoList.objects.all()
for list in video_lists:
    if list.community:
        CommunityVideoListPosition.objects.create(list=list.pk, community=list.community.pk)
    else:
        UserVideoListPosition.objects.create(list=list.pk, user=list.creator.pk)

good_lists = GoodList.objects.all()
for list in good_lists:
    if list.community:
        CommunityGoodListPosition.objects.create(list=list.pk, community=list.community.pk)
    else:
        UserGoodListPosition.objects.create(list=list.pk, user=list.creator.pk)

survey_lists = SurveyList.objects.all()
for list in survey_lists:
    if list.community:
        CommunitySurveyListPosition.objects.create(list=list.pk, community=list.community.pk)
    else:
        UserSurveyListPosition.objects.create(list=list.pk, user=list.creator.pk)

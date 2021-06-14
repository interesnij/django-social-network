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
from users.models import User
from users.model.list import *
from communities.models import Community
from communities.model.list import *


users = User.objects.all()
for user in users:
    post_lists = user.get_post_lists()
    for list in post_lists:
        if UserPostListPosition.objects.filter(user=user.pk, list=list.pk).exists():
            pass
        else:
            UserPostListPosition.objects.create(user=user.pk, list=list.pk, position=0)
    doc_lists = user.get_doc_lists()
    for list in doc_lists:
        if UserDocListPosition.objects.filter(user=user.pk, list=list.pk).exists():
            pass
        else:
            UserDocListPosition.objects.create(user=user.pk, list=list.pk, position=0)
    playlists = user.get_playlists()
    for list in playlists:
        if UserPlayListPosition.objects.filter(user=user.pk, list=list.pk).exists():
            pass
        else:
            UserPlayListPosition.objects.create(user=user.pk, list=list.pk, position=0)
    survey_lists = user.get_survey_lists()
    for list in survey_lists:
        if UserSurveyListPosition.objects.filter(user=user.pk, list=list.pk).exists():
            pass
        else:
            UserSurveyListPosition.objects.create(user=user.pk, list=list.pk, position=0)
    photo_lists = user.get_photo_lists()
    for list in photo_lists:
        if UserPhotoListPosition.objects.filter(user=user.pk, list=list.pk).exists():
            pass
        else:
            UserPhotoListPosition.objects.create(user=user.pk, list=list.pk, position=0)
    good_lists = user.get_good_lists()
    for list in good_lists:
        if UserGoodListPosition.objects.filter(user=user.pk, list=list.pk).exists():
            pass
        else:
            UserGoodListPosition.objects.create(user=user.pk, list=list.pk, position=0)
    video_lists = user.get_video_lists()
    for list in video_lists:
        if UserVideoListPosition.objects.filter(user=user.pk, list=list.pk).exists():
            pass
        else:
            UserVideoListPosition.objects.create(user=user.pk, list=list.pk, position=0)

communities = Community.objects.all()
for community in communities:
    post_lists = community.get_post_lists()
    for list in post_lists:
        if CommunityPostListPosition.objects.filter(community=community.pk, list=list.pk).exists():
            pass
        else:
            CommunityPostListPosition.objects.create(community=community.pk, list=list.pk, position=0)
    doc_lists = community.get_doc_lists()
    for list in doc_lists:
        if CommunityDocListPosition.objects.filter(community=community.pk, list=list.pk).exists():
            pass
        else:
            CommunityDocListPosition.objects.create(community=community.pk, list=list.pk, position=0)
    playlists = community.get_playlists()
    for list in playlists:
        if CommunityPlayListPosition.objects.filter(community=community.pk, list=list.pk).exists():
            pass
        else:
            CommunityPlayListPosition.objects.create(community=community.pk, list=list.pk, position=0)
    survey_lists = community.get_survey_lists()
    for list in survey_lists:
        if CommunitySurveyListPosition.objects.filter(community=community.pk, list=list.pk).exists():
            pass
        else:
            CommunitySurveyListPosition.objects.create(community=community.pk, list=list.pk, position=0)
    photo_lists = community.get_photo_lists()
    for list in photo_lists:
        if CommunityPhotoListPosition.objects.filter(community=community.pk, list=list.pk).exists():
            pass
        else:
            CommunityPhotoListPosition.objects.create(community=community.pk, list=list.pk, position=0)
    good_lists = community.get_good_lists()
    for list in good_lists:
        if CommunityGoodListPosition.objects.filter(community=community.pk, list=list.pk).exists():
            pass
        else:
            CommunityGoodListPosition.objects.create(community=community.pk, list=list.pk, position=0)
    video_lists = community.get_video_lists()
    for list in video_lists:
        if CommunityVideoListPosition.objects.filter(community=community.pk, list=list.pk).exists():
            pass
        else:
            CommunityVideoListPosition.objects.create(community=community.pk, list=list.pk, position=0)

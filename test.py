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
    order = 0
    posts = list.get_staff_items().order_by("created")
    list.count = list.count_items()
    list.save(update_fields=["count"])
    for post in posts:
        order += 1
        post.order = order
        post.save(update_fields=["order"])

users = User.objects.all()
for user in users:
    user.s_avatar = ''
    user.b_avatar = ''
    profile = UserProfile.objects.get(user=user)
    profile.posts = 0
    profile.tracks = 0
    profile.photos = 0
    profile.docs = 0
    user.save()
    profile.save()

communities = Community.objects.all()
for community in communities:
    community.s_avatar = ''
    community.b_avatar = ''
    community_info = CommunityInfo.objects.get(community=community)
    community_info.posts = 0
    community_info.tracks = 0
    community_info.photos = 0
    community_info.docs = 0
    community.save()
    community_info.save()

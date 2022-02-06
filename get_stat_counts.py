# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
from tinytag import TinyTag

django.setup()

from music.models import MusicList, Music
from video.models import VideoList, Video
from posts.models import PostsList, Post
from docs.models import DocsList, Doc
from gallery.models import PhotoList, Photo
from survey.models import SurveyList, Survey
from goods.models import GoodList, Good
from users.models import User
from users.model.list import *
from users.model.profile import *
from frends.models import Connect
from follows.models import Follow
from communities.models import Community
from communities.model.settings import CommunityInfo
from django.db.models import Q


for user in User.objects.all():
    profile = UserProfile.objects.get(user=user)
    profile.posts = Post.objects.filter(type="PUB", creator_id=user.pk, community=None).values("pk").count()
    profile.friends = Connect.objects.filter(user_id=user.pk).values("pk").count()
    profile.follows = Follow.objects.filter(followed_user_id=user.pk).values("pk").count()
    profile.communities = user.get_communities().values("pk").count()
    profile.photos = Photo.objects.filter(type="PUB", community=None, creator_id=user.pk).values("pk").count()
    profile.goods = Good.objects.filter(type="PUB", community=None, creator_id=user.pk).values("pk").count()
    profile.tracks = Music.objects.filter(type="PUB", community=None, creator_id=user.pk).values("pk").count()
    profile.videos = Video.objects.filter(type="PUB", community=None, creator_id=user.pk).values("pk").count()
    profile.docs = Doc.objects.filter(type="PUB", community=None, creator_id=user.pk).values("pk").count()
    profile.save()


for community in Community.objects.all():
    profile = CommunityInfo.objects.get(community=community)
    profile.posts = Post.objects.filter(type="PUB", community_id=community.pk).values("pk").count()
    profile.photos = Photo.objects.filter(type="PUB", community_id=community.pk).values("pk").count()
    profile.goods = Good.objects.filter(type="PUB", community_id=community.pk).values("pk").count()
    profile.tracks = Music.objects.filter(type="PUB", community_id=community.pk).values("pk").count()
    profile.videos = Video.objects.filter(type="PUB", community_id=community.pk).values("pk").count()
    profile.docs = Doc.objects.filter(type="PUB", community_id=community.pk).values("pk").count()
    profile.members = community.get_members(community.pk).values("pk").count()
    profile.save()

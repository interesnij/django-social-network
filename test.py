
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
from docs.models import DocsList, Doc
from posts.models import PostsList, Post
from communities.models import Community
from communities.model.list import CommunityDocsListPosition
from users.model.list import UserDocsListPosition
from users.models import User


UserDocsListPosition.objects.all().delete()
CommunityDocsListPosition.objects.all().delete()

for c in Community.objects.all():
    doc_list = DocsList.objects.create(creator=c.creator, community=c, type=DocsList.MAIN, name="Документы")
    CommunityDocsListPosition.objects.create(community=c.pk, list=c.get_doc_list().pk, position=1)

for u in User.objects.all():
    doc_list = DocsList.objects.create(creator=u, type=DocsList.MAIN, name="Документы")
    UserDocsListPosition.objects.create(user=u, list=c.get_doc_list().pk, position=1)

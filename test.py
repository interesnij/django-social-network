Skip to content
Search or jump to…
Pull requests
Issues
Marketplace
Explore

@interesnij
interesnij
/
rus
Public
1
00
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
rus/test.py /

Serg J
Latest commit 2d54834 3 hours ago
 History
 0 contributors
48 lines (34 sloc)  1.31 KB

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
from docs.models import DocsList
from posts.models import PostsList, Post
from communities.models import Community
from communities.model.list import CommunityDocsListPosition
from users.model.list import UserDocsListPosition
from users.models import User


Doc.objects.all().delete()

#for c in Community.objects.all():
#    doc_list = DocsList.objects.create(creator=c.creator, community=c, type=DocsList.MAIN, name="Документы")
#    CommunityDocsListPosition.objects.create(community=c.pk, list=c.get_doc_list().pk, position=1)

#for u in User.objects.all():
#    doc_list = DocsList.objects.create(creator=u, type=DocsList.MAIN, name="Документы")
#    UserDocsListPosition.objects.create(user=u, list=c.get_doc_list().pk, position=1)

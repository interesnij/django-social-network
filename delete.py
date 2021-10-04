# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from django.conf import settings
from docs.models import DocList
from music.models import SoundList, Music
from video.models import VideoList
from docs.models import Doc
from chat.models import Message
from gallery.models import PhotoList
from chat.models import Message
from communities.models import Community
from communities.model.settings import CommunityPrivate
import re

for c in Community.objects.all():
    CommunityPrivate.objects.create(community=c)

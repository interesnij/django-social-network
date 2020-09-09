# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from django.conf import settings
from users.models import User
from music.models import SoundList
from video.models import VideoAlbum
from docs.models import Doc2

Doc2.objects.all().delete()

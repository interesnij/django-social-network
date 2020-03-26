# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from django.conf import settings
from music.models import SoundList


SoundList.objects.create(creator_id=1, community=None, name="my_first_generic_playlist_number_12345678900000000") 

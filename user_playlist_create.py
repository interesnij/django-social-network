# -*- coding: utf-8 -*-
from locale import *
import sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from music.models import *

SoundList.objects.create(creator__pk=1, name="my_first_generic_playlist_number_12345678900000000")

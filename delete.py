# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
from tinytag import TinyTag

django.setup()

tag = TinyTag.get('/static/audio/event.mp3')
print('This track is by %s.' % tag.artist)
print('It is %f seconds long.' % tag.duration)

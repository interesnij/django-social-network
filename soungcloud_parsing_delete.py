# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django

django.setup()

from django.conf import settings
from music.models import *


SoundParsing.objects.all().delete()
SoundGenres.objects.all().delete()
SoundSymbol.objects.all().delete()
SoundList.objects.all().delete()
SoundTagsList.objects.all().delete()

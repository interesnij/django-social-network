# -*- coding: utf-8 -*-
from locale import *
import sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()

from music.models import *
from users.models import User

user = User.objects.get(pk=1)
list = SoundList.objects.filter(creator=user, name="my_first_generic_playlist_number_12345678900000000")
list.delete()

SoundList.objects.create(creator=user, name="my_first_generic_playlist_number_12345678900000000")

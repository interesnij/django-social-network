# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()

from django.conf import settings
from music.models import UserTempSoundList
from notifications.model.user import UserNotification, UserCommunityNotification
from notifications.model.item import ItemNotification, ItemCommunityNotification
from notifications.model.photo import PhotoNotification, PhotoCommunityNotification
from notifications.model.good import GoodNotification, GoodCommunityNotification

UserNotification.objects.all().delete()

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
from notifications.model2.user import UserNotification, UserCommunityNotification
from notifications.model2.item import ItemNotification, ItemCommunityNotification
from notifications.model2.photo import PhotoNotification, PhotoCommunityNotification
from notifications.model2.good import GoodNotification, GoodCommunityNotification

UserNotification.objects.all().delete()
UserCommunityNotification.objects.all().delete()
ItemNotification.objects.all().delete()
ItemCommunityNotification.objects.all().delete()
PhotoNotification.objects.all().delete()
PhotoCommunityNotification.objects.all().delete()
GoodNotification.objects.all().delete()
GoodCommunityNotification.objects.all().delete()

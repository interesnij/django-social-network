# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django

django.setup()

from django.conf import settings
from notifications.model.good import GoodNotification, GoodCommunityNotification
from notifications.model.user import UserNotification, UserCommunityNotification
from notifications.model.photo import PhotoNotification, PhotoCommunityNotification
from notifications.model.item import ItemNotification, ItemCommunityNotification

UserNotification.objects.all().delete()
UserCommunityNotification.objects.all().delete()
PhotoNotification.objects.all().delete()
PhotoCommunityNotification.objects.all().delete()
ItemNotification.objects.all().delete()
ItemCommunityNotification.objects.all().delete()

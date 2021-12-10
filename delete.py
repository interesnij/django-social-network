# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os
import urllib.request
import mimetypes

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()
import re
from users.model.list import *
from notify.models import *


for i in UserFeaturedFriend.objects.all():
    try:
        list = ListUC.objects.get(type=1, owner=i.user)
    except:
        list = ListUC.objects.create(type=1, name="Основной", owner=i.user)
    try:
        featured_user = FeaturedUC.objects.get(list=list, owner=i.user, user=i.featured_user)
    except:
        featured_user = FeaturedUC.objects.create(list=list, owner=i.user, user=i.featured_user)
    print(" Создано! ")

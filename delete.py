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
from users.models import User
from communities.models import Community


for user in User.objects.all():
    friends = user.get_all_connection()
    communities = user.get_communities()
    try:
        list = ListUC.objects.get(type=1, owner=user.pk)
    except:
        list = ListUC.objects.create(type=1, name="Основной", owner=user.pk)
    for frend in frends:
        try:
            NewsUC.objects.get(list=list, owner=user.pk, user=frend.pk)
        except:
            NewsUC.objects.create(list=list, owner=user.pk, user=frend.pk)

    for community in communities:
        try:
            NewsUC.objects.get(list=list, owner=user.pk, community=community.pk)
        except:
            NewsUC.objects.create(list=list, owner=user.pk, community=community.pk)

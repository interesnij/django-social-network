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
from communities.model.settings import *
from users.models import User
from communities.models import Community
from common.model.other import PhoneCodes

for user in User.objects.all():
    if user.phone < 1000:
        user.delete()

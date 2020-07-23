# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django, json, requests

django.setup()


from goods.models import Good, GoodSubCategory
from users.models import User

creator = User.objects.get(pk=1)
sub_category = GoodSubCategory.objects.get(order=1)
new_good = Good.create_good(title="Title", sub_category=sub_category, creator=creator, description="fdkgj ", community=None, price="1000", comments_enabled=True, votes_on=True, status="PG")

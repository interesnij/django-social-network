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
from notify.models import *

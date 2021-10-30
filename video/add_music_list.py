# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django, json, requests

django.setup()

import soundcloud
from music.models import *
from PIL import Image
from io import BytesIO
from django.core.files import File


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')

response = requests.get("https://api.soundcloud.com/resolve?url=https://soundcloud.com/yeonkkot/sets/s12&client_id=dce5652caa1b66331903493735ddd64d")
data = response.json()

if data:
    playlist_url = data['artwork_url']
    img_response = requests.get(url=playlist_url.replace("large.jpg", "crop.jpg"))
    img = Image.open(BytesIO(img_response.content))
    img.thumbnail((300, 300), Image.ANTIALIAS)
    thumb_io = BytesIO()
    img.save(thumb_io, img.format, quality=60)
    list = MusicList.objects.get(uuid='2759b12e-20ba-4214-85a6-0f303da28276')
    image = img.save(img.filename, quality=90)
    list.image.save(img.filename, ContentFile(thumb_io.getvalue()), save=False)
    list.save()

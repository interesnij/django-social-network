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
import io


client = soundcloud.Client(client_id='dce5652caa1b66331903493735ddd64d')
byteImgIO = io.BytesIO()

response = requests.get("https://api.soundcloud.com/resolve?url=https://soundcloud.com/yeonkkot/sets/s12&client_id=dce5652caa1b66331903493735ddd64d")
data = response.json()

if data:
    playlist_url = data['artwork_url']
    print(playlist_url)
    playlist_url.replace("large.jpg", "crop.jpg")
    print(playlist_url)
    img_response = requests.get(url=playlist_url).raw
    byteImg = Image.open(img_response)
    byteImg.save(byteImgIO, "JPG")
    byteImgIO.seek(0)
    byteImg = byteImgIO.read()
    print(byteImg)

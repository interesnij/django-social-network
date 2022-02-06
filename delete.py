# -*- coding: utf-8 -*-
from locale import *
import csv,sys,os

project_dir = '../tr/tr/'

sys.path.append(project_dir)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django
from tinytag import TinyTag

django.setup()

tag = TinyTag.get('static/audio/8mm - Around The Sun.mp3')
print('Исполнитель.', tag.artist)
print('Продолжительность', int(tag.duration)) 
print('Альбом.', tag.album)
print('Название', tag.title)
print('Жанр', tag.genre)

from django.urls import re_path
from main.view.items import *


urlpatterns = [
	re_path(r'^likes/$', ItemLikes.as_view()),
    re_path(r'^dislikes/$', ItemDislikes.as_view()),
]

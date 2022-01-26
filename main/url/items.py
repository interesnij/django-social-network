from django.conf.urls import url, include
from main.view.items import *


urlpatterns = [
	url(r'^likes/$', ItemLikes.as_view()),
    url(r'^dislikes/$', ItemDislikes.as_view()),
]

from django.conf.urls import url
from music.view.community import *


urlpatterns = [
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityLoadPlaylist.as_view()),
]

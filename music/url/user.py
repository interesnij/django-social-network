from django.conf.urls import url
from music.view.user import *


urlpatterns = [
    url(r'^load/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserLoadPlaylist.as_view()),
]

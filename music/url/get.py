from django.urls import re_path
from music.view.get import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    re_path(r'^genre/(?P<pk>\d+)/$', login_required(GenreMusicGet.as_view())),
    re_path(r'^list/(?P<pk>\d+)/$', login_required(ListMusicGet.as_view())),
]

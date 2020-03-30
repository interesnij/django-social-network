from django.conf.urls import url
from music.view.get import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^tag/(?P<pk>\d+)/$', login_required(TagMusicGet.as_view())),
]

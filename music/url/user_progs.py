from django.conf.urls import url
from music.view.user_progs import *


urlpatterns = [
    url(r'^souncloud_set_window/(?P<pk>\d+)/$', UserSoundcloudSetWindow.as_view()),
    url(r'^create_soundcloud_set/(?P<pk>\d+)/$', UserSoundcloudSetCreate.as_view()),
]

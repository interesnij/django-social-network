from django.conf.urls import url
from music.view.user_progs import *


urlpatterns = [
    url(r'^souncloud_create_list_window/(?P<pk>\d+)/$', UserSoundcloudSetPlaylistWindow.as_view()),
    url(r'^souncloud_list_window/(?P<pk>\d+)/$', UserSoundcloudSetWindow.as_view()),

    url(r'^create_soundcloud_set/(?P<pk>\d+)/$', UserSoundcloudSetCreate.as_view()),
    url(r'^soundcloud_set/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserSoundcloudSet.as_view()), 
]

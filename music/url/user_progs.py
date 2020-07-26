from django.conf.urls import url
from music.view.user_progs import *


urlpatterns = [
    url(r'^souncloud_create_list_window/(?P<pk>\d+)/$', UserSoundcloudSetPlaylistWindow.as_view()),
    url(r'^souncloud_list_window_main/(?P<pk>\d+)/$', UserSoundcloudSetMainWindow.as_view()),
    url(r'^souncloud_list_window/(?P<pk>\d+)/$', UserSoundcloudSetWindow.as_view()),

    url(r'^create_soundcloud_set/(?P<pk>\d+)/$', UserSoundcloudSetCreate.as_view()),
    url(r'^soundcloud_set_main/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserSoundcloudSetMain.as_view()),

    url(r'^u_add_track/(?P<pk>\d+)/$', login_required(UserTrackAdd.as_view())),
    url(r'^u_remove_track/(?P<pk>\d+)/$', login_required(UserTrackRemove.as_view())),
]

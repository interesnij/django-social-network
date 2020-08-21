from django.conf.urls import url
from music.view.community_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^souncloud_create_list_window/(?P<pk>\d+)/$', CommunitySoundcloudSetPlaylistWindow.as_view()),
    url(r'^souncloud_list_window/(?P<pk>\d+)/$', CommunitySoundcloudSetWindow.as_view()),
    url(r'^create_list_window/(?P<pk>\d+)/$', UserCreatePlaylistWindow.as_view()),

    url(r'^create_soundcloud_set/(?P<pk>\d+)/$', CommunitySoundcloudSetCreate.as_view()),
    url(r'^soundcloud_set/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunitySoundcloudSet.as_view()),

    url(r'^c_add_track/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackAdd.as_view())),
    url(r'^c_remove_track/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackRemove.as_view())),
    url(r'^c_add_track_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackListAdd.as_view())),
    url(r'^c_remove_track_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackListRemove.as_view())),
]

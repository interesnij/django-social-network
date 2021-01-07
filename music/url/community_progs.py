from django.conf.urls import url
from music.view.community_progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^souncloud_create_list_window/(?P<pk>\d+)/$', CommunitySoundcloudSetPlaylistWindow.as_view()),
    url(r'^souncloud_list_window/(?P<pk>\d+)/$', CommunitySoundcloudSetWindow.as_view()),
    url(r'^create_list_window/(?P<pk>\d+)/$', CommunityCreatePlaylistWindow.as_view()),
    url(r'^edit_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityEditPlaylistWindow.as_view()),

    url(r'^create_soundcloud_set/(?P<pk>\d+)/$', CommunitySoundcloudSetCreate.as_view()),
    url(r'^soundcloud_set/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunitySoundcloudSet.as_view()),
    url(r'^create_list/(?P<pk>\d+)/$', CommunityPlaylistCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPlaylistEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPlaylistDelete.as_view()),
    url(r'^abort_delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPlaylistAbortDelete.as_view()),
    url(r'^add_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPlaylistAdd.as_view()),
    url(r'^remove_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPlaylistRemove.as_view()),

    url(r'^c_add_track/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackAdd.as_view())),
    url(r'^c_remove_track/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackRemove.as_view())),
    url(r'^c_add_track_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackListAdd.as_view())),
    url(r'^c_remove_track_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityTrackListRemove.as_view())),
]

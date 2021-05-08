from django.conf.urls import url
from music.view.community_progs import *


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
    url(r'^restore_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPlaylistRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddPlayListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemovePlayListFromCommunityCollections.as_view()),

    url(r'^add_track_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddTrackInCommunityList.as_view()),
    url(r'^remove_track_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemoveTrackFromCommunityList.as_view()),
    url(r'^create_track/(?P<pk>\d+)/$', CommunityTrackCreate.as_view()),
    url(r'^edit_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackEdit.as_view()),
    url(r'^delete_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackRemove.as_view()),
    url(r'^restore_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackAbortRemove.as_view()),
]

from django.conf.urls import url
from music.view.user_progs import *


urlpatterns = [
    url(r'^add_list/(?P<pk>\d+)/$', UserPlaylistCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', UserPlaylistEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', UserPlaylistDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', UserPlaylistRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddPlayListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemovePlayListFromUserCollections.as_view()),
    url(r'^change_position/(?P<pk>\d+)/$', UserChangeMusicPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangeMusicListPosition.as_view()),

    url(r'^create_track/(?P<pk>\d+)/$', UserTrackCreate.as_view()),
    url(r'^edit_track/(?P<pk>\d+)/$', UserTrackEdit.as_view()),
    url(r'^delete_track/(?P<pk>\d+)/$', UserTrackRemove.as_view()),
    url(r'^restore_track/(?P<pk>\d+)/$', UserTrackAbortRemove.as_view()),
]

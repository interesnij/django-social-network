from django.conf.urls import url
from music.view.community_progs import *


urlpatterns = [
    url(r'^add_list/(?P<pk>\d+)/$', CommunityPlaylistCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/$', CommunityPlaylistEdit.as_view()),
    url(r'^delete_list/(?P<pk>\d+)/$', CommunityPlaylistDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/$', CommunityPlaylistRecover.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', AddPlayListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<list_pk>\d+)/$', RemovePlayListFromCommunityCollections.as_view()),
    
    url(r'^add_track/(?P<pk>\d+)/$', CommunityTrackCreate.as_view()),
    url(r'^edit_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackEdit.as_view()),
    url(r'^delete_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackRemove.as_view()),
    url(r'^restore_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackAbortRemove.as_view()),

    url(r'^change_position/(?P<pk>\d+)/$', CommunityChangeMusicPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', CommunityChangeMusicListPosition.as_view()),
]

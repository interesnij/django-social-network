from django.conf.urls import url
from music.view.community_progs import *


urlpatterns = [
    url(r'^add_track/(?P<pk>\d+)/$', CommunityTrackCreate.as_view()),
    url(r'^edit_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackEdit.as_view()),
    url(r'^delete_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackRemove.as_view()),
    url(r'^restore_track/(?P<pk>\d+)/(?P<track_pk>\d+)/$', CommunityTrackAbortRemove.as_view()),
]

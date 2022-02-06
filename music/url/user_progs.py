from django.conf.urls import url
from music.view.user_progs import *


urlpatterns = [
    url(r'^create_tracks/$', UserTracksCreate.as_view()),
    url(r'^edit_track/(?P<pk>\d+)/$', UserTrackEdit.as_view()),
    url(r'^delete_track/(?P<pk>\d+)/$', UserTrackRemove.as_view()),
    url(r'^restore_track/(?P<pk>\d+)/$', UserTrackAbortRemove.as_view()),
]

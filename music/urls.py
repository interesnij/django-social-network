from django.urls import re_path, include
from music.views import *


urlpatterns = [
    re_path(r'^$', AllMusicView.as_view(), name='all_music'),
    re_path(r'^genre/(?P<pk>\d+)/$', GenreMusicView.as_view(), name='genre_music'),
    re_path(r'^load_list/(?P<pk>\d+)/$', LoadMusiclist.as_view(), name="load_music_list"),

    re_path(r'^add_tracks_in_list/(?P<pk>\d+)/$', AddTrackInList.as_view()),
    re_path(r'^edit_track/(?P<pk>\d+)/$', TrackEdit.as_view()),
    re_path(r'^delete_track/(?P<pk>\d+)/$', TrackRemove.as_view()),
    re_path(r'^restore_track/(?P<pk>\d+)/$', TrackRestore.as_view()),

    re_path(r'^manage/', include('music.url.manage')),
    re_path(r'^get/', include('music.url.get')),
]

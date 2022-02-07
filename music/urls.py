from django.conf.urls import url, include
from music.views import *


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^genre/(?P<pk>\d+)/$', GenreMusicView.as_view(), name='genre_music'),
    url(r'^load_list/(?P<pk>\d+)/$', LoadMusiclist.as_view(), name="load_music_list"),

    url(r'^add_tracks_in_list/(?P<pk>\d+)/$', AddTrackInList.as_view()),
    url(r'^edit_track/(?P<pk>\d+)/$', TrackEdit.as_view()),
    url(r'^delete_track/(?P<pk>\d+)/$', TrackRemove.as_view()),
    url(r'^restore_track/(?P<pk>\d+)/$', TrackRestore.as_view()),

    url(r'^manage/', include('music.url.manage')),
    url(r'^get/', include('music.url.get')),
]

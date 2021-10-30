from django.conf.urls import url, include
from music.views import *


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^genre/(?P<pk>\d+)/$', GenreMusicView.as_view(), name='genre_music'),
    url(r'^load_list/(?P<pk>\d+)/$', LoadPlaylist.as_view(), name="load_music_list"),

    url(r'^manage/', include('music.url.manage')),
    url(r'^get/', include('music.url.get')),
    url(r'^user_progs/', include('music.url.user_progs')),
    url(r'^community_progs/', include('music.url.community_progs')),
    url(r'^repost/', include('music.url.repost')),
]

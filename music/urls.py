from django.conf.urls import url, include
from music.views import AllMusicView, AllSearchMusicView, AllTagsMusicView, AllTagMusicView, GenreMusicView


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^search_music/$', AllSearchMusicView.as_view(), name='search_all_music'),
    url(r'^tags/(?P<pk>\d+)/$', AllTagsMusicView.as_view(), name='tags_music'),
    url(r'^tag/(?P<pk>\d+)/$', AllTagMusicView.as_view(), name='tag_all_music'),
    url(r'^genre/(?P<pk>\d+)/$', GenreMusicView.as_view(), name='genre_music'),

    url(r'^manage/', include('music.url.manage')),
    url(r'^get/', include('music.url.get')),
    url(r'^user_progs/', include('music.url.user_progs')),
]

from django.conf.urls import url, include
from music.views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', AllMusicView.as_view(), name='all_music'),
    url(r'^search_music/$', AllSearchMusicView.as_view(), name='search_all_music'),
    url(r'^tags/(?P<pk>\d+)/$', AllTagsMusicView.as_view(), name='tags_music'),
    url(r'^tag/(?P<pk>\d+)/$', AllTagMusicView.as_view(), name='tag_all_music'),

    url(r'^list/', include('music.url.list')),
    url(r'^manage/', include('music.url.manage')),
]

from django.conf.urls import url
from music.view.list import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^all_music_list/$', AllMusicListView.as_view(), name='all_music_list_track'),
    url(r'^all_tag_list/(?P<pk>\d+)/$', AllTagListView.as_view(), name='tag_list_track'),
    url(r'^tag_list/(?P<pk>\d+)/$', TagsList.as_view(), name='tag_list'),
]

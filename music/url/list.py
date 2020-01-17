from django.conf.urls import url
from music.view.list import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^all_tag_list/(?P<pk>\d+)/$', TagList.as_view(), name='tag_list_track'),
    url(r'^tag_list/(?P<pk>\d+)/$', TagsList.as_view(), name='tag_list'),
    url(r'^genre_list/(?P<pk>\d+)/$', GenreList.as_view(), name='genre_list'),
]

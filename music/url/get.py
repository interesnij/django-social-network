from django.conf.urls import url
from music.view.get import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^tag/(?P<pk>\d+)/$', login_required(TagMusicGet.as_view())),
    url(r'^genre/(?P<pk>\d+)/$', login_required(GenreMusicGet.as_view())),
    url(r'^list/(?P<pk>\d+)/$', login_required(ListMusicGet.as_view())),

    url(r'^create_list_window/(?P<pk>\d+)/$', UserCreatePlaylistWindow.as_view()),
]

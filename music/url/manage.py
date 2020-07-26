from django.conf.urls import url
from music.view.manage import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^temp_list/(?P<pk>\d+)/$', login_required(TempListOn.as_view())),
    url(r'^temp_tag/(?P<pk>\d+)/$', login_required(TempTagOn.as_view())),
    url(r'^temp_genre/(?P<pk>\d+)/$', login_required(TempGenreOn.as_view())),

    url(r'^u_add_track/(?P<pk>\d+)/$', login_required(UserTrackAdd.as_view())),
    url(r'^u_remove_track/(?P<pk>\d+)/$', login_required(UserTrackRemove.as_view())),
    url(r'^create_list/(?P<pk>\d+)/$', UserPlaylistCreate.as_view()),
]

from django.conf.urls import url
from music.view.manage import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^temp_list/(?P<pk>\d+)/$', login_required(TempListOn.as_view())),
    url(r'^temp_tag/(?P<pk>\d+)/$', login_required(TempTagOn.as_view())),
    url(r'^my_list/$', login_required(MyListOn.as_view())),
    url(r'^add_track/(?P<pk>\d+)/$', login_required(TrackAdd.as_view())),
    url(r'^remove_track/(?P<pk>\d+)/$', login_required(TrackRemove.as_view())),
]

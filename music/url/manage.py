from django.conf.urls import url
from music.view.manage import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^temp_list/(?P<pk>\d+)/$', TempListOn.as_view(), name='temp_list_on'),
    url(r'^temp_tag/(?P<pk>\d+)/$', TempTagOn.as_view(), name='tag_list_on'),
    url(r'^my_list/(?P<pk>\d+)/$', MyListOn.as_view(), name='my_list_on'),
    url(r'^add_track/(?P<pk>\d+)/$', TrackAdd.as_view(), name='track_add'),
    url(r'^remove_track/(?P<pk>\d+)/$', TrackRemove.as_view(), name='track_remove'),
]

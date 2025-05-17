from django.urls import re_path
from communities.views.stat import *


urlpatterns = [
    re_path(r'^cuberture_year/(?P<pk>[0-9]+)/$', CommunityCoberturaYear.as_view(), name='community_cuberture_year'),
    re_path(r'^cuberture_month/(?P<pk>[0-9]+)/$', CommunityCoberturaMonth.as_view(), name='community_cuberture_month'),
    re_path(r'^cuberture_week/(?P<pk>[0-9]+)/$', CommunityCoberturaWeek.as_view(), name='community_cuberture_week'),
    re_path(r'^cuberture_day/(?P<pk>[0-9]+)/$', CommunityCoberturaDay.as_view(), name='community_cuberture_day'),

    re_path(r'^traffic_year/(?P<pk>[0-9]+)/$', CommunityTrafficYear.as_view(), name='community_traffic_year'),
    re_path(r'^traffic_month/(?P<pk>[0-9]+)/$', CommunityTrafficMonth.as_view(), name='community_traffic_month'),
    re_path(r'^traffic_week/(?P<pk>[0-9]+)/$', CommunityTrafficWeek.as_view(), name='community_traffic_week'),
    re_path(r'^traffic_day/(?P<pk>[0-9]+)/$', CommunityTrafficDay.as_view(), name='community_traffic_day'),
]

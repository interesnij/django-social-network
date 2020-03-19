from django.conf.urls import url, include
from communities.views.stat import *


urlpatterns = [
    url(r'^cuberture_month/(?P<pk>[0-9]+)/$', CommunityCoberturaMonth.as_view(), name='community_cuberture_month'),
    url(r'^cuberture_day/(?P<pk>[0-9]+)/$', CommunityCoberturaDay.as_view(), name='community_cuberture_day'),

    url(r'^traffic_month/(?P<pk>[0-9]+)/$', CommunityTrafficMonth.as_view(), name='community_traffic_month'),
    url(r'^traffic_day/(?P<pk>[0-9]+)/$', CommunityTrafficDay.as_view(), name='community_traffic_day'),
]

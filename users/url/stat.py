from django.conf.urls import url, include
from users.views.stat import *


urlpatterns = [
    url(r'^cuberture_year/(?P<pk>[0-9]+)/$', UserCoberturaYear.as_view(), name='user_cuberture_year'),
    url(r'^cuberture_month/(?P<pk>[0-9]+)/$', UserCoberturaMonth.as_view(), name='user_cuberture_month'),
    url(r'^cuberture_week/(?P<pk>[0-9]+)/$', UserCoberturaWeek.as_view(), name='user_cuberture_week'),
    url(r'^cuberture_day/(?P<pk>[0-9]+)/$', UserCoberturaDay.as_view(), name='user_cuberture_day'),

    url(r'^traffic_year/(?P<pk>[0-9]+)/$', UserTrafficYear.as_view(), name='user_traffic_year'),
    url(r'^traffic_month/(?P<pk>[0-9]+)/$', UserTrafficMonth.as_view(), name='user_traffic_month'),
    url(r'^traffic_week/(?P<pk>[0-9]+)/$', UserTrafficWeek.as_view(), name='user_traffic_week'),
    url(r'^traffic_day/(?P<pk>[0-9]+)/$', UserTrafficDay.as_view(), name='user_traffic_day'),
]

from django.conf.urls import url, include
from users.views.stat import *


urlpatterns = [
    url(r'^cuberture_year/$', UserCoberturaYear.as_view(), name='user_cuberture_year'),
    url(r'^cuberture_month/$', UserCoberturaMonth.as_view(), name='user_cuberture_month'),
    url(r'^cuberture_week/$', UserCoberturaWeek.as_view(), name='user_cuberture_week'),
    url(r'^cuberture_day/$', UserCoberturaDay.as_view(), name='user_cuberture_day'),

    url(r'^traffic_year/$', UserTrafficYear.as_view(), name='user_traffic_year'),
    url(r'^traffic_month/$', UserTrafficMonth.as_view(), name='user_traffic_month'),
    url(r'^traffic_week/$', UserTrafficWeek.as_view(), name='user_traffic_week'),
    url(r'^traffic_day/$', UserTrafficDay.as_view(), name='user_traffic_day'),
]

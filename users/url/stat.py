from django.urls import re_path
from users.views.stat import *


urlpatterns = [
    re_path(r'^cuberture_year/$', UserCoberturaYear.as_view(), name='user_cuberture_year'),
    re_path(r'^cuberture_month/$', UserCoberturaMonth.as_view(), name='user_cuberture_month'),
    re_path(r'^cuberture_week/$', UserCoberturaWeek.as_view(), name='user_cuberture_week'),
    re_path(r'^cuberture_day/$', UserCoberturaDay.as_view(), name='user_cuberture_day'),

    re_path(r'^traffic_year/$', UserTrafficYear.as_view(), name='user_traffic_year'),
    re_path(r'^traffic_month/$', UserTrafficMonth.as_view(), name='user_traffic_month'),
    re_path(r'^traffic_week/$', UserTrafficWeek.as_view(), name='user_traffic_week'),
    re_path(r'^traffic_day/$', UserTrafficDay.as_view(), name='user_traffic_day'),
]

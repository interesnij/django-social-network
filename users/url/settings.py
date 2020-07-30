from django.conf.urls import url
from users.views.settings import *


urlpatterns = [
    url(r'^general/(?P<pk>[0-9]+)/$', UserGeneralChange.as_view(), name='user_general_form'),
    url(r'^info/(?P<pk>[0-9]+)/$', UserInfoChange.as_view(), name='user_info_form'),
    url(r'^design/(?P<pk>\d+)/$', UserDesign.as_view(), name='user_design_form'),
    url(r'^notify/(?P<pk>[0-9]+)/$', SettingsNotifyView.as_view(), name='user_notify_form'),
] 

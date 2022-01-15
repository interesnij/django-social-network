from django.conf.urls import url
from users.views.progs import *


urlpatterns = [
    url(r'^block/(?P<pk>\d+)/$', UserBanCreate.as_view()),
    url(r'^unblock/(?P<pk>\d+)/$', UserUnbanCreate.as_view()),
    url(r'^color/(?P<color>[\w\-]+)/$', UserColorChange.as_view()),
    url(r'^phone_send/(?P<phone>\d+)/$', PhoneSend.as_view()),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', PhoneVerify.as_view()),
]

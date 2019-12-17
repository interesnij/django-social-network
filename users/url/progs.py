from django.conf.urls import url
from users.views.progs import UserBanCreate, UserUnbanCreate


urlpatterns = [
    url(r'^block(?P<pk>\d+)/$', UserBanCreate.as_view(), name='user_block'),
    url(r'^unblock(?P<pk>\d+)/$', UserUnbanCreate.as_view(), name='user_unblock'),
]

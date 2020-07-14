from django.conf.urls import url
from notify.view.good import *


urlpatterns = [
    url(r'^u/$', GoodNotificationListView.as_view()),
    url(r'^c/$', GoodCommunityNotificationListView.as_view()),
    url(r'^user_all_read/$', good_user_all_read, name='good_user_all_read'),
    url(r'^community_all_read/$', good_community_all_read, name='good_community_all_read'),
    url(r'^latest-notifications/$', good_get_latest_notifications),
]

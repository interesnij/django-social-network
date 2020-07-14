from django.conf.urls import url
from notify.view.user import *


urlpatterns = [
    url(r'^u/$', UserNotificationListView.as_view(), name='user_notify_list'),
    url(r'^c/$', CommunityNotificationListView.as_view(), name='community_notify_list'),
    url(r'^user_all_read/$', user_all_read, name='user_all_read'),
    url(r'^community_all_read/$', community_all_read, name='community_all_read'),
    url(r'^latest-notifications/$', get_latest_notifications, name='latest_notifications'),
]

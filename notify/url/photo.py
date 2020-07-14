from django.conf.urls import url

from notifications.view.photo import *


urlpatterns = [
    url(r'^u/$', PhotoNotificationListView.as_view()),
    url(r'^c/$', PhotoCommunityNotificationListView.as_view()),
    url(r'^user_all_read/$', photo_user_all_read, name='photo_user_all_read'),
    url(r'^community_all_read/$', photo_community_all_read, name='photo_community_all_read'),
    url(r'^latest-notifications/$', photo_get_latest_notifications),
]

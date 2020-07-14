from django.conf.urls import url

from notifications.view.item import *


urlpatterns = [
    url(r'^u/$', ItemNotificationListView.as_view()),
    url(r'^c/$', ItemCommunityNotificationListView.as_view()),
    url(r'^user_all_read/$', item_user_all_read, name='item_user_all_read'),
    url(r'^community_all_read/$', item_community_all_read, name='item_community_all_read'),
    url(r'^latest-notifications/$', item_get_latest_notifications),
]

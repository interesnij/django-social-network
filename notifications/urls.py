from django.conf.urls import url

from notifications import *


urlpatterns = [
    url(r'^$', NotificationUnreadListView.as_view(), name='unread'),
    url(r'^mark-as-read/(?P<slug>[-\w]+)/$', mark_as_read, name='mark_as_read'),
    url(r'^mark-all-as-read/$', mark_all_as_read, name='mark_all_read'),
    url(r'^latest-notifications/$', get_latest_notifications, name='latest_notifications'),
]

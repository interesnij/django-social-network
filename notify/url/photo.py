from django.conf.urls import url
from notify.view.photo import *


urlpatterns = [
    url(r'^u/$', PhotoNotificationListView.as_view()),
    url(r'^c/$', PhotoCommunityNotificationListView.as_view()),
    url(r'^latest_notifications/$', PhotoLastNotify.as_view()),
]

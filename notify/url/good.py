from django.conf.urls import url
from notify.view.good import *


urlpatterns = [
    url(r'^u/$', GoodNotificationListView.as_view()),
    url(r'^c/$', GoodCommunityNotificationListView.as_view()),
    url(r'^latest_notifications/$', GoodLastNotify.as_view()),
]

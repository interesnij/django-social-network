from django.conf.urls import url
from notify.view.post import *


urlpatterns = [
    url(r'', PostNotificationListView.as_view()),
    url(r'^c/$', PostCommunityNotificationListView.as_view()),
    url(r'^latest/$', PostLastNotify.as_view()),
]

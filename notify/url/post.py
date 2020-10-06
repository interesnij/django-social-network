from django.conf.urls import url
from notify.view.post import *


urlpatterns = [
    url(r'^u/$', PostNotificationListView.as_view()),
    url(r'^c/$', PostCommunityNotificationListView.as_view()),
    url(r'^user_all_read/$', post_user_all_read, name='post_user_all_read'),
    url(r'^community_all_read/$', post_community_all_read, name='post_community_all_read'),
    url(r'^latest/$', PostLastNotify.as_view()),
]

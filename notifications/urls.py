from django.conf.urls import url

from notifications import views


urlpatterns = [
    url(r'^user/$', views.UserNotificationListView.as_view(), name='user_notify_list'),
    url(r'^user/$', views.CommunityNotificationListView.as_view(), name='community_notify_list'),
    url(r'^user_all_read/$', views.user_all_read, name='user_all_read'),
    url(r'^community_all_read/$', views.community_all_read, name='community_all_read'),
    url(r'^latest-notifications/$', views.get_latest_notifications, name='latest_notifications'),
    url(r'^clean-notifications/$', views.NotificationCleanView.as_view(), name='clean_notifications'),
]

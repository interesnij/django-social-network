from notifications.views import NotificationsView
from django.conf.urls import url

urlpatterns = [
    url(r'^notifications/$', NotificationsView.as_view(), name='notifications')
]

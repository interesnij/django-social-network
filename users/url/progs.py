from django.conf.urls import url
from users.views.progs import UserBanCreate, UserUnbanCreate, UserColorChange


urlpatterns = [
    url(r'^block/(?P<pk>\d+)/$', UserBanCreate.as_view()),
    url(r'^unblock/(?P<pk>\d+)/$', UserUnbanCreate.as_view()),
    url(r'^color/<color>/$', UserColorChange.as_view()),
]

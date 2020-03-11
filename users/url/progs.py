from django.conf.urls import url
from users.views.progs import UserBanCreate, UserUnbanCreate, UserColorChange, UserItemView


urlpatterns = [
    url(r'^block/(?P<pk>\d+)/$', UserBanCreate.as_view()),
    url(r'^unblock/(?P<pk>\d+)/$', UserUnbanCreate.as_view()),
    url(r'^color/(?P<color>[\w\-]+)/$', UserColorChange.as_view()),
    url(r'^item_view/(?P<pk>\d+)/$', UserItemView.as_view()),
]

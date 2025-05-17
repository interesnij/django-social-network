from frends.views import *
from django.urls import re_path


urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', FrendsListView.as_view(), name="frends"),
    re_path(r'^online/(?P<pk>\d+)/$', OnlineFrendsListView.as_view(), name="online_frends"),
    re_path(r'^common/(?P<pk>\d+)/$', CommonFrendsListView.as_view(), name="common_frends"),

    re_path(r'^add/(?P<pk>\d+)/$', ConnectCreate.as_view(), name="create_connect"),
    re_path(r'^delete/(?P<pk>\d+)/$', ConnectDelete.as_view(), name="delete_connect"),
]

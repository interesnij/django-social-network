from django.urls import re_path
from follows.views import *


urlpatterns = [
    re_path(r'^(?P<pk>\d+)/$', FollowsView.as_view(), name='follows'),
    re_path(r'^out/$', FollowingsView.as_view(), name='followings'),
    re_path(r'^add/(?P<pk>\d+)/$', FollowCreate.as_view()),
    re_path(r'^view/(?P<pk>\d+)/$', FollowView.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/$', FollowDelete.as_view()),
    re_path(r'^add_member/(?P<pk>\d+)/$', CommunityFollowCreate.as_view()),
    re_path(r'^delete_member/(?P<pk>\d+)/$', CommunityFollowDelete.as_view()),
    re_path(r'^community_view/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityFollowView.as_view()),
]

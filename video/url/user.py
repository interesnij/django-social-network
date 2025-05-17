from django.urls import re_path
from video.view.user import *


urlpatterns = [
    re_path(r'^list/(?P<pk>\d+)/$', UserVideoList.as_view()),
    re_path(r'^list_post/(?P<pk>\d+)/$', UserPostVideoList.as_view()),
    re_path(r'^list_message/(?P<pk>\d+)/$', UserMessageVideoList.as_view()),
    re_path(r'^list_post_comment/(?P<pk>\d+)/$', UserPostCommentVideoList.as_view()),
    re_path(r'^detail/(?P<pk>\d+)/(?P<video_pk>\d+)/$', UserVideoDetail.as_view(), name="video_detail"),
    re_path(r'^info/(?P<pk>\d+)/$', UserVideoInfo.as_view()),
]

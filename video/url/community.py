from django.urls import re_path
from video.view.community import *


urlpatterns = [
    re_path(r'^list/(?P<pk>\d+)/$', CommunityVideoList.as_view()),
    re_path(r'^list_post/(?P<pk>\d+)/$', CommunityPostVideoList.as_view()),
    re_path(r'^list_post_comment/(?P<pk>\d+)/$', CommunityPostCommentVideoList.as_view()),
    re_path(r'^detail/(?P<pk>\d+)/(?P<video_pk>\d+)/$', CommunityVideoDetail.as_view(), name="video_detail"),
    re_path(r'^info/(?P<pk>\d+)/(?P<video_pk>\d+)/$', CommunityVideoInfo.as_view()),
]

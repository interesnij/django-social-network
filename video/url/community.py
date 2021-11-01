from django.conf.urls import url
from video.view.community import *


urlpatterns = [
    url(r'^list/(?P<pk>\d+)/$', CommunityVideoList.as_view()),
    url(r'^list_post/(?P<pk>\d+)/$', CommunityPostVideoList.as_view()),
    url(r'^list_post_comment/(?P<pk>\d+)/$', CommunityPostCommentVideoList.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<video_pk>\d+)/$', CommunityVideoDetail.as_view(), name="video_detail"),
    url(r'^info/(?P<pk>\d+)/(?P<video_pk>\d+)/$', CommunityVideoInfo.as_view()),
]

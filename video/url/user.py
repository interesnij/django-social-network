from django.conf.urls import url
from video.view.user import *


urlpatterns = [
    url(r'^list/(?P<pk>\d+)/$', UserVideoList.as_view()),
    url(r'^list_post/(?P<pk>\d+)/$', UserPostVideoList.as_view()),
    url(r'^list_message/(?P<pk>\d+)/$', UserMessageVideoList.as_view()),
    url(r'^list_post_comment/(?P<pk>\d+)/$', UserPostCommentVideoList.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<video_pk>\d+)/$', UserVideoDetail.as_view(), name="video_detail"),
    url(r'^info/(?P<pk>\d+)/$', UserVideoInfo.as_view()),
]

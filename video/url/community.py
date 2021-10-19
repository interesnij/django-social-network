from django.conf.urls import url
from video.view.community import *


urlpatterns = [
    url(r'^list/(?P<pk>\d+)/$', CommunityVideoList.as_view()),
    url(r'^list_post/(?P<uuid>[0-9a-f-]+)/$', CommunityPostVideoList.as_view()),
    url(r'^list_post_comment/(?P<pk>\d+)/$', CommunityPostCommentVideoList.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoDetail.as_view(), name="video_detail"),
    url(r'^info/(?P<pk>\d+)/(?P<video_pk>\d+)/$', CommunityVideoInfo.as_view()),
]

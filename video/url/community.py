from django.conf.urls import url
from video.view.community import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoList.as_view()),
    url(r'^list_post/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPostVideoList.as_view()),
    url(r'^list_post_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', CommunityPostCommentVideoList.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoDetail.as_view(), name="video_detail"),
    url(r'^info/(?P<pk>\d+)/(?P<video_pk>\d+)/$', CommunityVideoInfo.as_view()),

    url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', VideoCommunityCommentList.as_view()),
]

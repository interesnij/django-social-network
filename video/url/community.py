from django.conf.urls import url
from video.view.community_progs import *


urlpatterns = [
    url(r'^list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoList.as_view()),
    url(r'^detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoDetail.as_view(), name="u_video_detail"),

    url(r'^create_list_window/(?P<pk>\d+)/$', CommunityCreateListWindow.as_view()),
    url(r'^create_video_attach_window/(?P<pk>\d+)/$', CommunityCreateVideoAttachWindow.as_view()),
    url(r'^create_video_list_window/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityCreateVideoListWindow.as_view()),
]

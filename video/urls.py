from django.urls import re_path, include
from video.views import *


urlpatterns = [
    re_path(r'^$', AllVideoView.as_view()),
    re_path(r'^load_list/(?P<pk>\d+)/$', LoadVideoList.as_view(), name="load_video_list"),

    re_path(r'^add_video_in_list/(?P<pk>\d+)/$', VideoCreate.as_view()),
    re_path(r'^edit_video/$', VideoEdit.as_view()),

    re_path(r'^user/', include('video.url.user')),
    re_path(r'^community/', include('video.url.community')),

    re_path(r'^user_progs/', include('video.url.user_progs')),
    re_path(r'^community_progs/', include('video.url.community_progs')),
]

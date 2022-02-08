from django.conf.urls import url, include
from video.views import *


urlpatterns = [
    url(r'^$', AllVideoView.as_view()),
    url(r'^load_list/(?P<pk>\d+)/$', LoadVideoList.as_view(), name="load_video_list"),

    url(r'^add_video_in_list/(?P<pk>\d+)/$', VideoCreate.as_view()),
    url(r'^edit_video/(?P<pk>\d+)/$', VideoEdit.as_view()),

    url(r'^user/', include('video.url.user')),
    url(r'^community/', include('video.url.community')),

    url(r'^user_progs/', include('video.url.user_progs')),
    url(r'^community_progs/', include('video.url.community_progs')),
]

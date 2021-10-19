from django.conf.urls import url, include
from video.views import *


urlpatterns = [
    url(r'^$', AllVideoView.as_view()),
    url(r'^load_list/(?P<pk>\d+)/$', LoadVideoList.as_view(), name="load_video_list"),
    url(r'^comments/(?P<uuid>[0-9a-f-]+)/$', VideoCommentList.as_view()),

    url(r'^user/', include('video.url.user')),
    url(r'^community/', include('video.url.community')),

    url(r'^user_progs/', include('video.url.user_progs')),
    url(r'^community_progs/', include('video.url.community_progs')),

    url(r'^votes/', include('video.url.votes')),
	url(r'^window/', include('video.url.window')),

    url(r'^repost/', include('video.url.repost')),
]

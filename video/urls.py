from django.conf.urls import url, include
from video.views import AllVideoView


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),

    url(r'^user_progs/', include('video.url.user_progs')),
    url(r'^community_progs/', include('video.url.community_progs')),
    url(r'^user/', include('video.url.user')),
    url(r'^community/', include('video.url.community')),
    url(r'^votes/', include('video.url.votes')),
	url(r'^window/', include('video.url.window')),
]

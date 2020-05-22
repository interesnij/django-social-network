from django.conf.urls import url, include
from video.views import AllVideoView


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),

    url(r'^progs/', include('video.url.progs')),
    url(r'^user/', include('video.url.user')),
]

from django.conf.urls import url
from video.views import AllVideoView


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),
    url(r'^get_video_playlist/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoPlaylist.as_view()),
]

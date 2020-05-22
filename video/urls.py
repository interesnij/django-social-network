from django.conf.urls import url
from video.views import AllVideoView, UserBasicVideoList, UserVideoList, 


urlpatterns = [
    url(r'^$', AllVideoView.as_view(), name='all_video'),
    url(r'^user_basic_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserBasicVideoList.as_view()),
    url(r'^user_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view()),
]

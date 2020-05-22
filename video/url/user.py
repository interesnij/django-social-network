from django.conf.urls import url, include
from video.view.user import UserBasicVideoList, UserVideoList


urlpatterns = [
    url(r'^basic_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserBasicVideoList.as_view()),
    url(r'^list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view()),
]

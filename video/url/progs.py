from django.conf.urls import url
from video.view.progs import UserVideoListCreate, UserVideoInListCreate, UserVideoAttachCreate


urlpatterns = [
    url(r'^create_list/(?P<pk>\d+)/$', UserVideoListCreate.as_view()),
    url(r'^create_video_attach/(?P<pk>\d+)/$', UserVideoAttachCreate.as_view()),
    url(r'^create_video_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoInListCreate.as_view()),
]

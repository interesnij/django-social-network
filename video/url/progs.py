from django.conf.urls import url
from video.view.progs import UserVideoListCreate, UserVideoCreate


urlpatterns = [
    url(r'^create_list/(?P<pk>\d+)/$', UserVideoListCreate.as_view()),
    url(r'^create_video/(?P<pk>\d+)/$', UserVideoCreate.as_view()),
]

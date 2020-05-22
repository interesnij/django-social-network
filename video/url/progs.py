from django.conf.urls import url, include
from video.view.progs import UserVideoListCreate, UserVideoList


urlpatterns = [
    url(r'^create_list/(?P<pk>\d+)/$', UserVideoListCreate.as_view()),
]

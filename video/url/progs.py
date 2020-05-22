from django.conf.urls import url
from video.view.progs import UserVideoListCreate


urlpatterns = [
    url(r'^create_list/(?P<pk>\d+)/$', UserVideoListCreate.as_view()),
]

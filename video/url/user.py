from django.conf.urls import url
from video.view.user import UserBasicVideoList, UserVideoList, UserCreateListWindow


urlpatterns = [
    url(r'^basic_list/(?P<pk>\d+)/$', UserBasicVideoList.as_view()),
    url(r'^list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserVideoList.as_view()),
    url(r'^create_list_window/(?P<pk>\d+)/$', UserCreateListWindow.as_view()),
]

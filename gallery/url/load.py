from gallery.view.load import *
from django.conf.urls import url


urlpatterns=[
    url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhoto.as_view(), name='user_photo'),
    url(r'^avatar_detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserDetailAvatar.as_view(), name='user_detail_avatar'),
]

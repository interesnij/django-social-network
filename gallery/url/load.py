from gallery.view.load import *
from django.conf.urls import url


urlpatterns=[
    url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhoto.as_view()),
    url(r'^u_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/(?P<album_uuid>[0-9a-f-]+)/$', UserAlbumPhoto.as_view()),
    url(r'^comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserCommentPhoto.as_view()),
    url(r'^avatar_detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserDetailAvatar.as_view()),
]

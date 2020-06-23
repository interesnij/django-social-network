from gallery.view.load import *
from django.conf.urls import url


urlpatterns=[
    url(r'^user_photo/(?P<uuid>[0-9a-f-]+)/$', UserPhoto.as_view(), name="user_photo"),
    url(r'^user_album_photo/(?P<pk>\d+)/(?P<album_uuid>[0-9a-f-]+)/$', UserAlbumPhoto.as_view(), name="user_album_photo"),
    url(r'^user_wall/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserWallPhoto.as_view(), name="u_wall_photo"),
    url(r'^avatar_detail/(?P<uuid>[0-9a-f-]+)/$', UserDetailAvatar.as_view(), name="user_avatar"),
    url(r'^community_avatar_detail/(?P<uuid>[0-9a-f-]+)/$', CommunityDetailAvatar.as_view(), name="community_avatar"),
    url(r'^community_photo/(?P<uuid>[0-9a-f-]+)/$', CommunityPhoto.as_view(), name="community_photo"),
    url(r'^community_album_photo/(?P<pk>\d+)/(?P<album_uuid>[0-9a-f-]+)/$', UserAlbumPhoto.as_view(), name="user_album_photo"),
    url(r'^community_wall/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserWallPhoto.as_view(), name="u_wall_photo"),

]

from gallery.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^photos/(?P<pk>\d+)/$', UserPhotosList.as_view()),
	url(r'^album_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAlbumPhotosList.as_view(), name="user_photos"),

	url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhoto.as_view(), name="user_photo"),
    url(r'^album_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAlbumPhoto.as_view(), name="user_album_photo"),
    url(r'^wall_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserWallPhoto.as_view(), name="u_wall_photo"),
    url(r'^avatar_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserDetailAvatar.as_view(), name="user_avatar"),
	url(r'^avatar/(?P<pk>\d+)/$', UserFirstAvatar.as_view()),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),

	url(r'^comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoUserCommentList.as_view()),
]

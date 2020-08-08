from gallery.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', UserGalleryView.as_view(), name="user_gallery"),
	url(r'^photos/(?P<uuid>[0-9a-f-]+)/$', UserPhotosList.as_view()),
	url(r'^album_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAlbumPhotosList.as_view(), name="user_photos"),
	url(r'^album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAlbumView.as_view(), name="user_album"),

	url(r'^add_photo/(?P<pk>\d+)/$', PhotoUserCreate.as_view()),
	url(r'^add_comment_photo/(?P<pk>\d+)/$', PhotoAttachUserCreate.as_view()),
	url(r'^add_album_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoAlbumUserCreate.as_view(), name="photo_album_add_user"),
	url(r'^add_album/(?P<pk>\d+)/$', AlbumUserCreate.as_view(), name="album_add_user"),

	url(r'^add_avatar/(?P<pk>\d+)/$', UserAddAvatar.as_view()),

	url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhoto.as_view(), name="user_photo"),
    url(r'^album_photo/(?P<pk>\d+)/(?P<album_uuid>[0-9a-f-]+)/$', UserAlbumPhoto.as_view(), name="user_album_photo"),
    url(r'^wall/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserWallPhoto.as_view(), name="u_wall_photo"),
    url(r'^avatar/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserDetailAvatar.as_view(), name="user_avatar"),
]

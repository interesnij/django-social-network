from gallery.views.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', UserGalleryView.as_view(), name="user_gallery"),
	url(r'^album/reload/(?P<uuid>[0-9a-f-]+)/$', UserAlbomReload.as_view(), name="user_album"),
	url(r'^albums/(?P<uuid>[0-9a-f-]+)/$', UserAlbumsList.as_view(), name="user_albums"),
	url(r'^photos/(?P<uuid>[0-9a-f-]+)/$', UserPhotosList.as_view(), name="user_photos"),
	url(r'^album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAlbomView.as_view(), name="user_album"),
	url(r'^add_photo/(?P<uuid>[0-9a-f-]+)/$', PhotoUserCreate.as_view(), name="photo_add_user"),
	url(r'^add_album/(?P<uuid>[0-9a-f-]+)/$', AlbumUserCreate.as_view(), name="album_add_user"),
	url(r'^gygyg/(?P<uuid>[0-9a-f-]+)/$', AlbomGygView.as_view(), name="album_ggg"),

	url(r'^add_avatar/(?P<pk>\d+)/$', UserAddAvatar.as_view(), name='user_add_avatar'),
	url(r'^avatar-reload/(?P<pk>\d+)/$', AvatarReload.as_view(), name='avatar_reload'),
]

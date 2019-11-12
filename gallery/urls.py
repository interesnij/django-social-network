from gallery.views import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', GalleryView.as_view(), name="gallery"),
	url(r'^user_album/(?P<uuid>[0-9a-f-]+)/$', UserAlbomView.as_view(), name="user_album"),
	url(r'^user_album/reload/(?P<uuid>[0-9a-f-]+)/$', UserAlbomReload.as_view(), name="user_album"),
	url(r'^user_albums/(?P<uuid>[0-9a-f-]+)/$', UserAlbumsList.as_view(), name="user_albums"),
	url(r'^user_photos/(?P<uuid>[0-9a-f-]+)/$', UserPhotosList.as_view(), name="user_photos"),
	url(r'^add_photo/(?P<uuid>[0-9a-f-]+)/$', UserPhoto.as_view(), name="photo_user"),
	url(r'^add_album/(?P<uuid>[0-9a-f-]+)/$', AlbumUserCreate.as_view(), name="album_add_user"),
	url(r'^gygyg/(?P<uuid>[0-9a-f-]+)/$', AlbomGygView.as_view(), name="album_ggg"),
	url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoView.as_view(), name='user_photo'),
]

from gallery.views import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', GalleryView.as_view(), name="gallery"),
	url(r'^album/(?P<uuid>[0-9a-f-]+)/$', AlbomView.as_view(), name="album"),
	url(r'^album/reload/(?P<uuid>[0-9a-f-]+)/$', AlbomReloadView.as_view(), name="album"),
	url(r'^albums/(?P<uuid>[0-9a-f-]+)/$', AlbumsListView.as_view(), name="albums"),
	url(r'^photos/(?P<uuid>[0-9a-f-]+)/$', PhotosListView.as_view(), name="photos"),
	url(r'^add_photo/(?P<uuid>[0-9a-f-]+)/$', PhotoUserCreate.as_view(), name="photo_add_user"),
	url(r'^add_album/(?P<uuid>[0-9a-f-]+)/$', AlbumUserCreate.as_view(), name="album_add_user"),
	url(r'^gygyg/(?P<uuid>[0-9a-f-]+)/$', AlbomGygView.as_view(), name="album_ggg"),
	url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoView.as_view(), name='user_photo'),
]

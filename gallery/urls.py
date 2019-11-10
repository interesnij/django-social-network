from gallery.views import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', GalleryView.as_view(), name="gallery"),
	url(r'^album/(?P<uuid>[0-9a-f-]+)/$', AlbomView.as_view(), name="album"),
	url(r'^albums/(?P<uuid>[0-9a-f-]+)/$', AlbumsListView.as_view(), name="albums"),
	url(r'^photos/(?P<uuid>[0-9a-f-]+)/$', PhotosListView.as_view(), name="photos"),
]

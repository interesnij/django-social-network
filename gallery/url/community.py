from gallery.view.community import *
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', CommunityGalleryView.as_view(), name="community_gallery"),
	url(r'^album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbomView.as_view(), name="community_album"),
	url(r'^photos/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotosList.as_view(), name="community_photos"),
	url(r'^add_photo/(?P<uuid>[0-9a-f-]+)/$', PhotoCommunityCreate.as_view(), name="photo_add_community"),
	url(r'^add_album/(?P<uuid>[0-9a-f-]+)/$', AlbumCommunityCreate.as_view(), name="album_add_community"),
	url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhoto.as_view(), name='community_photo'),
]

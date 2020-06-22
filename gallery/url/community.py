from gallery.view.community import *
from django.conf.urls import url

urlpatterns=[
	url(r'^(?P<pk>\d+)/$', CommunityGalleryView.as_view(), name="community_gallery"),
	url(r'^photos/(?P<pk>\d+)/$', CommunityPhotosList.as_view()),
	url(r'^album_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumPhotosList.as_view(), name="community_photos"),
	url(r'^album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumView.as_view(), name="community_album"),

	url(r'^add_photo/(?P<pk>\d+)/$', PhotoCommunityCreate.as_view()),
	url(r'^add_comment_photo/(?P<pk>\d+)/$', CommunityAttachUserCreate.as_view()),
	url(r'^add_album_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumUserCreate.as_view()),
	url(r'^add_album/(?P<pk>\d+)/$', AlbumCommunityCreate.as_view()),

	url(r'^add_avatar/(?P<pk>\d+)/$', CommunityAddAvatar.as_view()),
]

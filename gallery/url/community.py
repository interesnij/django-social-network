from gallery.view.community import *
from django.conf.urls import url

urlpatterns=[
	url(r'^(?P<pk>\d+)/$', CommunityGalleryView.as_view(), name="community_gallery"),
	url(r'^photos/(?P<pk>\d+)/$', CommunityPhotosList.as_view()),
	url(r'^album_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumPhotosList.as_view(), name="community_photos"),
	url(r'^album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumView.as_view(), name="community_album"),

	url(r'^add_photo/(?P<pk>\d+)/$', PhotoCommunityCreate.as_view()),
	url(r'^add_comment_photo/(?P<pk>\d+)/$', PhotoAttachCommunityCreate.as_view()),
	url(r'^add_album_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoAlbumCommunityCreate.as_view()),
	url(r'^add_album/(?P<pk>\d+)/$', AlbumCommunityCreate.as_view()),

	url(r'^add_avatar/(?P<pk>\d+)/$', CommunityAddAvatar.as_view()),

	url(r'^avatar_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityDetailAvatar.as_view(), name="community_avatar"),
    url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhoto.as_view(), name="community_photo"),
    url(r'^album_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumPhoto.as_view(), name="community_album_photo"),
    url(r'^wall_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityWallPhoto.as_view(), name="c_wall_photo"),
	url(r'^avatar/(?P<pk>\d+)/$', CommunityFirstAvatar.as_view()),
]

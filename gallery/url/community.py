from gallery.view.community import *
from django.conf.urls import url

urlpatterns=[
	url(r'^photos/(?P<pk>\d+)/$', CommunityPhotosList.as_view(), name="community_photo_list_load"),
	url(r'^list_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumPhotosList.as_view(), name="community_photos_load"),
	url(r'^post_photo/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', CommunityPostPhoto.as_view(), name="community_post_photo"),
	url(r'^avatar/(?P<pk>\d+)/$', CommunityFirstAvatar.as_view()),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetCommunityPhoto.as_view()),
	url(r'^chat_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', CommunityChatPhoto.as_view(), name="community_chat_photo"),

	url(r'^comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoCommunityCommentList.as_view()),
]

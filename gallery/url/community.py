from gallery.view.community import *
from django.conf.urls import url

urlpatterns=[
	url(r'^photos/(?P<pk>\d+)/$', CommunityPhotosList.as_view()),
	url(r'^list_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumPhotoList.as_view(), name="community_photos"),

	url(r'^avatar_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', CommunityDetailAvatar.as_view(), name="community_avatar"), 
    url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhoto.as_view(), name="community_photo"),
    url(r'^list_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityAlbumPhotoList.as_view(), name="community_list_photo"),
	url(r'^post_photo/(?P<uuid>[0-9a-f-]+)/(?P<photo_pk>\d+)/$', CommunityPostPhoto.as_view(), name="community_post_photo"),
	url(r'^avatar/(?P<pk>\d+)/$', CommunityFirstAvatar.as_view()),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetCommunityPhoto.as_view()),
	url(r'^chat_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', CommunityChatPhoto.as_view(), name="community_chat_photo"),

	url(r'^comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoCommunityCommentList.as_view()),
]

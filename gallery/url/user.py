from gallery.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^photos/(?P<pk>\d+)/$', UserPhotosList.as_view()),
	url(r'^list_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoAlbumList.as_view(), name="user_photos"),

	url(r'^photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhoto.as_view(), name="user_photo"),
    url(r'^list_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoAlbumList.as_view(), name="user_list_photo"),
    url(r'^wall_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserWallPhoto.as_view(), name="u_wall_photo"),
    url(r'^avatar_photo/(?P<photo_pk>\d+)/$', UserDetailAvatar.as_view(), name="user_avatar"),
	url(r'^post_photo/(?P<uuid>[0-9a-f-]+)/(?P<photo_pk>\d+)/$', UserPostPhoto.as_view(), name="user_post_photo"),
	url(r'^comment_photo/(?P<pk>\d+)/$', UserCommentPhoto.as_view(), name="user_comment_photo"),
	url(r'^avatar/(?P<pk>\d+)/$', UserFirstAvatar.as_view()),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),
	url(r'^chat_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserChatPhoto.as_view(), name="user_chat_photo"),

	url(r'^comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoUserCommentList.as_view()),
	url(r'^load/(?P<uuid>[0-9a-f-]+)/$', UserLoadPhotoList.as_view()),
]

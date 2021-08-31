from gallery.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^photos/(?P<pk>\d+)/$', UserPhotosList.as_view()),
	url(r'^list_photos/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotosAlbumList.as_view(), name="user_photos"),

	url(r'^avatar/(?P<pk>\d+)/$', UserFirstAvatar.as_view()),
	url(r'^post_photo/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', UserPostPhoto.as_view(), name="user_post_photo"),
	url(r'^comment_photo/(?P<pk>\d+)/$', UserCommentPhoto.as_view(), name="user_comment_photo"),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),

	url(r'^comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoUserCommentList.as_view()),
	url(r'^load/(?P<uuid>[0-9a-f-]+)/$', UserLoadPhotoList.as_view()), name="user_load_photo_list",
]

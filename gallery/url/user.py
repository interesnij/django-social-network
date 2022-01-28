from gallery.view.user import *
from django.conf.urls import url


urlpatterns=[
	url(r'^list_photos/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UserPhotosAlbumList.as_view(), name="user_photos_load"),
	url(r'^comment_photo/(?P<pk>\d+)/$', UserCommentPhoto.as_view(), name="user_comment_photo"),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),
]

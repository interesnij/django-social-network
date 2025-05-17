from gallery.view.user import *
from django.urls import re_path


urlpatterns=[
	re_path(r'^comment_photo/(?P<pk>\d+)/$', UserCommentPhoto.as_view(), name="user_comment_photo"),
	re_path(r'^preview_photo/(?P<pk>\d+)/$', GetUserPhoto.as_view()),
]

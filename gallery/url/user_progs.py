from gallery.view.user_progs import *
from django.urls import re_path


urlpatterns=[
    re_path(r'^description/(?P<pk>\d+)/$', UserPhotoDescription.as_view()),
    re_path(r'^delete/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserPhotoDelete.as_view()),
    re_path(r'^restore/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserPhotoRecover.as_view()),
    re_path(r'^on_comment/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOpenCommentPhoto.as_view()),
    re_path(r'^off_comment/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserCloseCommentPhoto.as_view()),
    re_path(r'^on_votes/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOnVotesPhoto.as_view()),
    re_path(r'^off_votes/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOffVotesPhoto.as_view()),

    re_path(r'^add_attach_photo/$', PhotoAttachUserCreate.as_view()),
	re_path(r'^add_avatar/(?P<pk>\d+)/$', UserAddAvatar.as_view()),
]

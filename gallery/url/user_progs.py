from gallery.view.user_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^description/(?P<pk>\d+)/$', UserPhotoDescription.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserPhotoDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserPhotoRecover.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOpenCommentPhoto.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserCloseCommentPhoto.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOnVotesPhoto.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOffVotesPhoto.as_view()),

    url(r'^add_attach_photo/$', PhotoAttachUserCreate.as_view()),
	url(r'^add_avatar/(?P<pk>\d+)/$', UserAddAvatar.as_view()),
]

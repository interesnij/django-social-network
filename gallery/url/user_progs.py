from gallery.view.user_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^description/(?P<pk>\d+)/$', UserPhotoDescription.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserPhotoDelete.as_view()), 
    url(r'^restore/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserPhotoRecover.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOpenCommentPhoto.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserCloseCommentPhoto.as_view()),
    url(r'^on_private/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOnPrivatePhoto.as_view()),
    url(r'^off_private/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOffPrivatePhoto.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOnVotesPhoto.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', UserOffVotesPhoto.as_view()),

    url(r'^add_comment/$', login_required(PhotoCommentUserCreate.as_view())),
    url(r'^reply_comment/$', login_required(PhotoReplyUserCreate.as_view())),
    url(r'^edit_comment/(?P<pk>\d+)/$', PhotoUserCommentEdit.as_view()),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(PhotoCommentUserDelete.as_view())),
	url(r'^restore_comment/(?P<pk>\d+)/$', login_required(PhotoCommentUserRecover.as_view())),
    url(r'^add_attach_photo/$', PhotoAttachUserCreate.as_view()),
	url(r'^add_avatar/(?P<pk>\d+)/$', UserAddAvatar.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', PhotoListUserCreate.as_view()),
    url(r'^edit_list/(?P<list_pk>\d+)/$', PhotoListUserEdit.as_view()),
    url(r'^delete_list/(?P<list_pk>\d+)/$', PhotoListUserDelete.as_view()),
    url(r'^restore_list/(?P<list_pk>\d+)/$', PhotoListUserRecover.as_view()),
    url(r'^add_photo_in_list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', AddPhotoInUserList.as_view()),
    url(r'^remove_photo_from_list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', RemovePhotoFromUserList.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/$', AddPhotoListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/$', RemovePhotoListFromUserCollections.as_view()),
    url(r'^change_position/(?P<pk>\d+)/$', UserChangePhotoPosition.as_view()),
	url(r'^change_list_position/(?P<pk>\d+)/$', UserChangePhotoListPosition.as_view()),
]

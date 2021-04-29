from gallery.view.user_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^description/(?P<uuid>[0-9a-f-]+)/$', UserPhotoDescription.as_view()),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', UserPhotoDelete.as_view()),
    url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', UserPhotoAbortDelete.as_view()),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', UserOpenCommentPhoto.as_view()),
    url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', UserCloseCommentPhoto.as_view()),
    url(r'^on_private/(?P<uuid>[0-9a-f-]+)/$', UserOnPrivatePhoto.as_view()),
    url(r'^off_private/(?P<uuid>[0-9a-f-]+)/$', UserOffPrivatePhoto.as_view()),
    url(r'^on_votes/(?P<uuid>[0-9a-f-]+)/$', UserOnVotesPhoto.as_view()),
    url(r'^off_votes/(?P<uuid>[0-9a-f-]+)/$', UserOffVotesPhoto.as_view()),

    url(r'^post-comment/$', login_required(PhotoCommentUserCreate.as_view())),
    url(r'^reply-comment/$', login_required(PhotoReplyUserCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(PhotoCommentUserDelete.as_view())),
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(PhotoCommentUserAbortDelete.as_view())),
    url(r'^delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PhotoWallCommentUserDelete.as_view())),
	url(r'^abort_delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PhotoWallCommentUserAbortDelete.as_view())),

    url(r'^add_photo/(?P<pk>\d+)/$', PhotoUserCreate.as_view()),
    url(r'^add_attach_photo/(?P<pk>\d+)/$', PhotoAttachUserCreate.as_view()),
	url(r'^add_comment_photo/(?P<pk>\d+)/$', PhotoAttachUserCreate.as_view()),
	url(r'^add_list_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoListUserCreate.as_view(), name="photo_list_add_user"),
	url(r'^add_avatar/(?P<pk>\d+)/$', UserAddAvatar.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', PhotoListUserCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoListUserEdit.as_view(), name="photo_list_edit_user"),
    url(r'^delete_list/(?P<uuid>[0-9a-f-]+)/$', PhotoListUserDelete.as_view()),
    url(r'^abort_delete_list/(?P<uuid>[0-9a-f-]+)/$', PhotoListUserAbortDelete.as_view()),
    url(r'^add_photo_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoListAdd.as_view()),
    url(r'^remove_photo_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoListRemove.as_view()),
    url(r'^add_list_in_collections/(?P<uuid>[0-9a-f-]+)/$', AddPhotoListInUserCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<uuid>[0-9a-f-]+)/$', RemovePhotoListFromUserCollections.as_view()),
]

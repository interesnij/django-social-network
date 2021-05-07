from gallery.view.community_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^description/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotoDescription.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotoDelete.as_view()),
    url(r'^restore/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotoAbortDelete.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOpenCommentPhoto.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityCloseCommentPhoto.as_view()),
    url(r'^on_private/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOnPrivatePhoto.as_view()),
    url(r'^off_private/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOffPrivatePhoto.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesPhoto.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesPhoto.as_view()),

    url(r'^post-comment/$', login_required(PhotoCommentCommunityCreate.as_view())),
    url(r'^reply-comment/$', login_required(PhotoReplyCommunityCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(PhotoCommentCommunityDelete.as_view())),
	url(r'^restore_comment/(?P<pk>\d+)/$', login_required(PhotoCommentCommunityAbortDelete.as_view())),
    url(r'^delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PhotoWallCommentCommunityDelete.as_view())),
	url(r'^restore_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PhotoWallCommentCommunityAbortDelete.as_view())),

    url(r'^add_photo/(?P<pk>\d+)/$', PhotoCommunityCreate.as_view()),
	url(r'^add_attach_photo/(?P<pk>\d+)/$', PhotoAttachCommunityCreate.as_view()),
	url(r'^add_list_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoListCommunityCreate.as_view()),
	url(r'^add_avatar/(?P<pk>\d+)/$', CommunityAddAvatar.as_view()),
    url(r'^add_photo_in_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddPhotoInCommunityList.as_view()),
    url(r'^remove_photo_from_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemovePhotoFromCommunityList.as_view()),

    url(r'^add_list/(?P<pk>\d+)/$', PhotoListCommunityCreate.as_view()),
    url(r'^edit_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoListCommunityEdit.as_view(), name="photo_list_edit_community"),
    url(r'^delete_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoListCommunityDelete.as_view()),
    url(r'^restore_list/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoListCommunityAbortDelete.as_view()),
    url(r'^add_list_in_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AddPhotoListInCommunityCollections.as_view()),
    url(r'^remove_list_from_collections/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RemovePhotoListFromCommunityCollections.as_view()),
]

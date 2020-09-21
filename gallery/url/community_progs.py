from gallery.view.community_progs import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns=[
    url(r'^description/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotoDescription.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotoDelete.as_view()),
    url(r'^abort_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotoAbortDelete.as_view()),
    url(r'^on_comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOpenCommentPhoto.as_view()),
    url(r'^off_comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityCloseCommentPhoto.as_view()),
    url(r'^on_private/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOnPrivatePhoto.as_view()),
    url(r'^off_private/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOffPrivatePhoto.as_view()),
    url(r'^on_votes/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOnVotesPhoto.as_view()),
    url(r'^off_votes/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityOffVotesPhoto.as_view()),

    url(r'^comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoCommunityCommentList.as_view()),
    url(r'^post-comment/$', login_required(PhotoCommentCommunityCreate.as_view())),
    url(r'^reply-comment/$', login_required(PhotoReplyCommunityCreate.as_view())),
    url(r'^delete_comment/(?P<pk>\d+)/$', login_required(PhotoCommentCommunityDelete.as_view())),
	url(r'^abort_delete_comment/(?P<pk>\d+)/$', login_required(PhotoCommentCommunityAbortDelete.as_view())),
    url(r'^delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PhotoWallCommentCommunityDelete.as_view())),
	url(r'^abort_delete_wall_comment/(?P<pk>\d+)/(?P<comment_pk>\d+)/$', login_required(PhotoWallCommentCommunityAbortDelete.as_view())),

    url(r'^add_photo/(?P<pk>\d+)/$', PhotoCommunityCreate.as_view()),
	url(r'^add_attach_photo/(?P<pk>\d+)/$', PhotoAttachCommunityCreate.as_view()),
	url(r'^add_album_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', PhotoAlbumCommunityCreate.as_view()),
	url(r'^add_avatar/(?P<pk>\d+)/$', CommunityAddAvatar.as_view()),

    url(r'^add_album/(?P<pk>\d+)/$', AlbumCommunityCreate.as_view()),
    url(r'^edit_album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AlbumCommunityEdit.as_view(), name="photo_album_edit_community"),
    url(r'^delete_album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AlbumCommunityDelete.as_view()),
    url(r'^abort_delete_album/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', AlbumCommunityAbortDelete.as_view()),
]

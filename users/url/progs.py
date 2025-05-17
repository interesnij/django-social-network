from django.urls import re_path
from users.views.progs import *


urlpatterns = [
    re_path(r'^block/(?P<pk>\d+)/$', UserBanCreate.as_view()),
    re_path(r'^unblock/(?P<pk>\d+)/$', UserUnbanCreate.as_view()),
    re_path(r'^color/(?P<color>[\w\-]+)/$', UserColorChange.as_view()),
    re_path(r'^phone_send/(?P<phone>\d+)/$', PhoneSend.as_view()),
    re_path(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', PhoneVerify.as_view()),

    re_path(r'^add_comment/$', CommentUserCreate.as_view()),
    re_path(r'^reply_comment/$', ReplyUserCreate.as_view()),
    re_path(r'^like_comment/$', CommentLikeCreate.as_view()),
    re_path(r'^dislike_comment/$', CommentDislikeCreate.as_view()),
    re_path(r'^like_item/$', ItemLikeCreate.as_view()),
    re_path(r'^dislike_item/$', ItemDislikeCreate.as_view()),
    re_path(r'^edit_comment/$', CommentEdit.as_view()),
    re_path(r'^delete_comment/$', CommentDelete.as_view()),
    re_path(r'^recover_comment/$', CommentRecover.as_view()),
    re_path(r'^create_repost/$', RepostCreate.as_view()),
    re_path(r'^create_claim/$', ClaimCreate.as_view()),

    re_path(r'^create_copy/$', CopyCreate.as_view()),
    re_path(r'^uncopy_user_list/$', UserListUncopy.as_view()),
    re_path(r'^uncopy_community_list/(?P<pk>\d+)/$', CommunityListUncopy.as_view()),

    re_path(r'^create_list/$', ListCreate.as_view()),
    re_path(r'^edit_list/$', ListEdit.as_view()),
    re_path(r'^delete_list/$', ListDelete.as_view()),
    re_path(r'^recover_list/$', ListRecover.as_view()),

    re_path(r'^change_position/(?P<pk>\d+)/$', ChangeListPosition.as_view()),
]

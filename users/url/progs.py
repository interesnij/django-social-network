from django.conf.urls import url
from users.views.progs import *


urlpatterns = [
    url(r'^block/(?P<pk>\d+)/$', UserBanCreate.as_view()),
    url(r'^unblock/(?P<pk>\d+)/$', UserUnbanCreate.as_view()),
    url(r'^color/(?P<color>[\w\-]+)/$', UserColorChange.as_view()),
    url(r'^phone_send/(?P<phone>\d+)/$', PhoneSend.as_view()),
    url(r'^phone_verify/(?P<phone>\d+)/(?P<code>\d+)/$', PhoneVerify.as_view()),

    url(r'^add_comment/$', CommentUserCreate.as_view()),
    url(r'^reply_comment/$', ReplyUserCreate.as_view()),
    url(r'^like_comment/$', CommentLikeCreate.as_view()),
    url(r'^dislike_comment/$', CommentDislikeCreate.as_view()),
    url(r'^like_item/$', ItemLikeCreate.as_view()),
    url(r'^dislike_item/$', ItemDislikeCreate.as_view()),
    url(r'^edit_comment/$', CommentEdit.as_view()),
    url(r'^delete_comment/$', CommentDelete.as_view()),
    url(r'^recover_comment/$', CommentRecover.as_view()),
    url(r'^create_repost/$', RepostCreate.as_view()),
    url(r'^create_claim/$', ClaimCreate.as_view()),
    url(r'^create_copy/$', CopyCreate.as_view()),

    url(r'^create_list/$', ListCreate.as_view()),
    url(r'^edit_list/$', ListEdit.as_view()),
    url(r'^delete_list/$', ListDelete.as_view()),
    url(r'^recover_list/$', ListRecover.as_view()),

    url(r'^change_position/(?P<pk>\d+)/$', ChangeListPosition.as_view()),
]

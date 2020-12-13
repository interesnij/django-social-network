from django.conf.urls import url
from managers.view.moderation_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/$', login_required(ModerationUserList.as_view())),
    url(r'^community/$', login_required(ModerationCommunityList.as_view())),
    url(r'^post/$', login_required(ModerationPostList.as_view())),
    url(r'^photo/$', login_required(ModerationPhotoList.as_view())),
    url(r'^good/$', login_required(ModerationGoodList.as_view())),
    url(r'^audio/$', login_required(ModerationAudioList.as_view())),
    url(r'^video/$', login_required(ModerationVideoList.as_view())),

    url(r'^post_comment/$', login_required(ModerationPostCommentList.as_view())),
    url(r'^photo_comment/$', login_required(ModerationPhotoCommentList.as_view())),
    url(r'^good_comment/$', login_required(ModerationGoodCommentList.as_view())),
    url(r'^video_comment/$', login_required(ModerationVideoCommentList.as_view())),

    url(r'^user_advertiser/$', login_required(ModerationUserAdvertiserList.as_view())),
    url(r'^community_advertiser/$', login_required(ModerationCommunityAdvertiserList.as_view())),
]

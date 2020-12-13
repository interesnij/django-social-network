from django.conf.urls import url
from managers.view.penalty_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/$', login_required(PenaltyUserList.as_view())),
    url(r'^community/$', login_required(PenaltyCommunityList.as_view())),
    url(r'^post/$', login_required(PenaltyPostList.as_view())),
    url(r'^photo/$', login_required(PenaltyPhotoList.as_view())),
    url(r'^good/$', login_required(PenaltyGoodList.as_view())),
    url(r'^audio/$', login_required(PenaltyAudioList.as_view())),
    url(r'^video/$', login_required(PenaltyVideoList.as_view())),

    url(r'^post_comment/$', login_required(PenaltyPostCommentList.as_view())),
    url(r'^photo_comment/$', login_required(PenaltyPhotoCommentList.as_view())),
    url(r'^good_comment/$', login_required(PenaltyGoodCommentList.as_view())),
    url(r'^video_comment/$', login_required(PenaltyVideoCommentList.as_view())),

    url(r'^user_advertiser/$', login_required(PenaltyUserAdvertiserList.as_view())),
    url(r'^community_advertiser/$', login_required(PenaltyCommunityAdvertiserList.as_view())),
]

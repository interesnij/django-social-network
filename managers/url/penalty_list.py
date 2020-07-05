from django.conf.urls import url
from managers.view.penalty_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/(?P<pk>\d+)/$', login_required(PenaltyUserList.as_view())),
    url(r'^community/(?P<pk>\d+)/$', login_required(PenaltyCommunityList.as_view())),
    url(r'^post/(?P<pk>\d+)/$', login_required(PenaltyPostList.as_view())),
    url(r'^photo/(?P<pk>\d+)/$', login_required(PenaltyPhotoList.as_view())),
    url(r'^good/(?P<pk>\d+)/$', login_required(PenaltyGoodList.as_view())),
    url(r'^audio/(?P<pk>\d+)/$', login_required(PenaltyAudioList.as_view())),
    url(r'^video/(?P<pk>\d+)/$', login_required(PenaltyVideoList.as_view())),

    url(r'^post_comment/(?P<pk>\d+)/$', login_required(PenaltyPostCommentList.as_view())),
    url(r'^photo_comment/(?P<pk>\d+)/$', login_required(PenaltyPhotoCommentList.as_view())),
    url(r'^good_comment/(?P<pk>\d+)/$', login_required(PenaltyGoodCommentList.as_view())),
    url(r'^audio_comment/(?P<pk>\d+)/$', login_required(PenaltyAudioCommentList.as_view())),
    url(r'^video_comment/(?P<pk>\d+)/$', login_required(PenaltyVideoCommentList.as_view())),

    url(r'^user_advertiser/(?P<pk>\d+)/$', login_required(PenaltyUserAdvertiserList.as_view())),
    url(r'^community_advertiser/(?P<pk>\d+)/$', login_required(PenaltyCommunityAdvertiserList.as_view())),
]

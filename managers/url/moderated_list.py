from django.conf.urls import url
from managers.view.moderation_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user/(?P<pk>\d+)/$', login_required(ModerationUserList.as_view())),
    url(r'^community/(?P<pk>\d+)/$', login_required(ModerationCommunityList.as_view())),
    url(r'^post/(?P<pk>\d+)/$', login_required(ModerationPostList.as_view())),
    url(r'^photo/(?P<pk>\d+)/$', login_required(ModerationPhotoList.as_view())),
    url(r'^good/(?P<pk>\d+)/$', login_required(ModerationGoodList.as_view())),
    url(r'^audio/(?P<pk>\d+)/$', login_required(ModerationAudioList.as_view())),
    url(r'^video/(?P<pk>\d+)/$', login_required(ModerationAdminList.as_view())),

    url(r'^post_comment/(?P<pk>\d+)/$', login_required(ModerationPostCommentList.as_view())),
    url(r'^photo_comment/(?P<pk>\d+)/$', login_required(ModerationPhotoCommentList.as_view())),
    url(r'^good_comment/(?P<pk>\d+)/$', login_required(ModerationGoodCommentList.as_view())),
    url(r'^audio_comment/(?P<pk>\d+)/$', login_required(ModerationAudioCommentList.as_view())),
    url(r'^video_comment/(?P<pk>\d+)/$', login_required(ModerationVideoCommentList.as_view())),

    url(r'^user_advertiser/(?P<pk>\d+)/$', login_required(ModerationUserAdvertiserList.as_view())),
    url(r'^community_advertiser/(?P<pk>\d+)/$', login_required(ModerationCommunityAdvertiserList.as_view())),
]

from django.conf.urls import url
from managers.view.penalty_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user_admin/(?P<pk>\d+)/$', login_required(PenaltyUserAdminList.as_view())),
    url(r'^community_admin/(?P<pk>\d+)/$', login_required(PenaltyCommunityAdminList.as_view())),
    url(r'^post_admin/(?P<pk>\d+)/$', login_required(PenaltyPostAdminList.as_view())),
    url(r'^photo_admin/(?P<pk>\d+)/$', login_required(PenaltyPhotoAdminList.as_view())),
    url(r'^good_admin/(?P<pk>\d+)/$', login_required(PenaltyGoodAdminList.as_view())),
    url(r'^audio_admin/(?P<pk>\d+)/$', login_required(PenaltyAudioAdminList.as_view())),
    url(r'^video_admin/(?P<pk>\d+)/$', login_required(PenaltyVideoAdminList.as_view())),

    url(r'^user_editor/(?P<pk>\d+)/$', login_required(PenaltyUserEditorList.as_view())),
    url(r'^community_editor/(?P<pk>\d+)/$', login_required(PenaltyCommunityEditorList.as_view())),
    url(r'^post_editor/(?P<pk>\d+)/$', login_required(PenaltyPostEditorList.as_view())),
    url(r'^photo_editor/(?P<pk>\d+)/$', login_required(PenaltyPhotoEditorList.as_view())),
    url(r'^good_editor/(?P<pk>\d+)/$', login_required(PenaltyGoodEditorList.as_view())),
    url(r'^audio_editor/(?P<pk>\d+)/$', login_required(PenaltyAudioEditorList.as_view())),
    url(r'^video_editor/(?P<pk>\d+)/$', login_required(PenaltyVideoEditorList.as_view())),

    url(r'^user_moderator/(?P<pk>\d+)/$', login_required(PenaltyUserModeratorList.as_view())),
    url(r'^community_moderator/(?P<pk>\d+)/$', login_required(PenaltyCommunityModeratorList.as_view())),
    url(r'^post_moderator/(?P<pk>\d+)/$', login_required(PenaltyPostModeratorList.as_view())),
    url(r'^photo_moderator/(?P<pk>\d+)/$', login_required(PenaltyPhotoModeratorList.as_view())),
    url(r'^good_moderator/(?P<pk>\d+)/$', login_required(PenaltyGoodModeratorList.as_view())),
    url(r'^audio_moderator/(?P<pk>\d+)/$', login_required(PenaltyAudioModeratorList.as_view())),
    url(r'^video_moderator/(?P<pk>\d+)/$', login_required(PenaltyVideoModeratorList.as_view())),

    url(r'^user_advertiser/(?P<pk>\d+)/$', login_required(PenaltyUserAdvertiserList.as_view())),
    url(r'^community_advertiser/(?P<pk>\d+)/$', login_required(PenaltyCommunityAdvertiserList.as_view())),
]

from django.conf.urls import url
from managers.view.moderation_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user_admin/(?P<pk>\d+)/$', login_required(ModerationUserAdminList.as_view())),
    url(r'^community_admin/(?P<pk>\d+)/$', login_required(ModerationCommunityAdminList.as_view())),
    url(r'^post_admin/(?P<pk>\d+)/$', login_required(ModerationPostAdminList.as_view())),
    url(r'^photo_admin/(?P<pk>\d+)/$', login_required(ModerationPhotoAdminList.as_view())),
    url(r'^good_admin/(?P<pk>\d+)/$', login_required(ModerationGoodAdminList.as_view())),
    url(r'^audio_admin/(?P<pk>\d+)/$', login_required(ModerationAudioAdminList.as_view())),
    url(r'^video_admin/(?P<pk>\d+)/$', login_required(ModerationVideoAdminList.as_view())),

    url(r'^user_editor/(?P<pk>\d+)/$', login_required(ModerationUserEditorList.as_view())),
    url(r'^community_editor/(?P<pk>\d+)/$', login_required(ModerationCommunityEditorList.as_view())),
    url(r'^post_editor/(?P<pk>\d+)/$', login_required(ModerationPostEditorList.as_view())),
    url(r'^photo_editor/(?P<pk>\d+)/$', login_required(ModerationPhotoEditorList.as_view())),
    url(r'^good_editor/(?P<pk>\d+)/$', login_required(ModerationGoodEditorList.as_view())),
    url(r'^audio_editor/(?P<pk>\d+)/$', login_required(ModerationAudioEditorList.as_view())),
    url(r'^video_editor/(?P<pk>\d+)/$', login_required(ModerationVideoEditorList.as_view())),

    url(r'^user_moderator/(?P<pk>\d+)/$', login_required(ModerationUserModeratorList.as_view())),
    url(r'^community_moderator/(?P<pk>\d+)/$', login_required(ModerationCommunityModeratorList.as_view())),
    url(r'^post_moderator/(?P<pk>\d+)/$', login_required(ModerationPostModeratorList.as_view())),
    url(r'^photo_moderator/(?P<pk>\d+)/$', login_required(ModerationPhotoModeratorList.as_view())),
    url(r'^good_moderator/(?P<pk>\d+)/$', login_required(ModerationGoodModeratorList.as_view())),
    url(r'^audio_moderator/(?P<pk>\d+)/$', login_required(ModerationAudioModeratorList.as_view())),
    url(r'^video_moderator/(?P<pk>\d+)/$', login_required(ModerationVideoModeratorList.as_view())),

    url(r'^user_advertiser/(?P<pk>\d+)/$', login_required(ModerationUserAdvertiserList.as_view())),
    url(r'^community_advertiser/(?P<pk>\d+)/$', login_required(ModerationCommunityAdvertiserList.as_view())),
]

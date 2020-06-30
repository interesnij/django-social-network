from django.conf.urls import url
from managers.view.penalty_list import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^user_admin/(?P<pk>\d+)/$', login_required(UserAdminList.as_view())),
    url(r'^community_admin/(?P<pk>\d+)/$', login_required(CommunityAdminList.as_view())),
    url(r'^post_admin/(?P<pk>\d+)/$', login_required(PostAdminList.as_view())),
    url(r'^photo_admin/(?P<pk>\d+)/$', login_required(PhotoAdminList.as_view())),
    url(r'^good_admin/(?P<pk>\d+)/$', login_required(GoodAdminList.as_view())),
    url(r'^audio_admin/(?P<pk>\d+)/$', login_required(AudioAdminList.as_view())),
    url(r'^video_admin/(?P<pk>\d+)/$', login_required(VideoAdminList.as_view())),

    url(r'^user_editor/(?P<pk>\d+)/$', login_required(UserEditorList.as_view())),
    url(r'^community_editor/(?P<pk>\d+)/$', login_required(CommunityEditorList.as_view())),
    url(r'^post_editor/(?P<pk>\d+)/$', login_required(PostEditorList.as_view())),
    url(r'^photo_editor/(?P<pk>\d+)/$', login_required(PhotoEditorList.as_view())),
    url(r'^good_editor/(?P<pk>\d+)/$', login_required(GoodEditorList.as_view())),
    url(r'^audio_editor/(?P<pk>\d+)/$', login_required(AudioEditorList.as_view())),
    url(r'^video_editor/(?P<pk>\d+)/$', login_required(VideoEditorList.as_view())),

    url(r'^user_moderator/(?P<pk>\d+)/$', login_required(UserModeratorList.as_view())),
    url(r'^community_moderator/(?P<pk>\d+)/$', login_required(CommunityModeratorList.as_view())),
    url(r'^post_moderator/(?P<pk>\d+)/$', login_required(PostModeratorList.as_view())),
    url(r'^photo_moderator/(?P<pk>\d+)/$', login_required(PhotoModeratorList.as_view())),
    url(r'^good_moderator/(?P<pk>\d+)/$', login_required(GoodModeratorList.as_view())),
    url(r'^audio_moderator/(?P<pk>\d+)/$', login_required(AudioModeratorList.as_view())),
    url(r'^video_moderator/(?P<pk>\d+)/$', login_required(VideoModeratorList.as_view())),

    url(r'^user_advertiser/(?P<pk>\d+)/$', login_required(UserAdvertiserList.as_view())),
    url(r'^community_advertiser/(?P<pk>\d+)/$', login_required(CommunityAdvertiserList.as_view())),
]

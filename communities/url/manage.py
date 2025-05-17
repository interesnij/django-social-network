from django.urls import re_path
from communities.views.manage import *


urlpatterns = [
    re_path(r'^general/(?P<pk>[0-9]+)/$', CommunityGeneralView.as_view(), name='community_general_form'),
    re_path(r'^private/(?P<pk>[0-9]+)/$', CommunitySectionsOpenView.as_view(), name='community_sections_form'),

    re_path(r'^notify_post/(?P<pk>[0-9]+)/$', CommunityNotifyPostView.as_view(), name='community_post_notify'),
    re_path(r'^notify_photo/(?P<pk>[0-9]+)/$', CommunityNotifyPhotoView.as_view(), name='community_photo_notify'),
    re_path(r'^notify_good/(?P<pk>[0-9]+)/$', CommunityNotifyGoodView.as_view(), name='community_good_notify'),
    re_path(r'^notify_video/(?P<pk>[0-9]+)/$', CommunityNotifyVideoView.as_view(), name='community_video_notify'),
    re_path(r'^notify_music/(?P<pk>[0-9]+)/$', CommunityNotifyMusicView.as_view(), name='community_music_notify'),

    re_path(r'^(?P<pk>[0-9]+)/admins/$', CommunityAdminView.as_view(), name='community_admins'),
    re_path(r'^(?P<pk>[0-9]+)/moders/$', CommunityModersView.as_view(), name='community_moders'),
    re_path(r'^(?P<pk>[0-9]+)/black_list/$', CommunityBlackListView.as_view(), name='community_black_list'),
    re_path(r'^(?P<pk>[0-9]+)/follows/$', CommunityFollowsView.as_view(), name='community_follows'),
    re_path(r'^(?P<pk>[0-9]+)/members/$', CommunityMemberManageView.as_view(), name='community_member_manage'),
    re_path(r'^(?P<pk>[0-9]+)/editors/$', CommunityEditorsView.as_view(), name='community_editors'),
    re_path(r'^(?P<pk>[0-9]+)/rekl/$', CommunityAdvertisersView.as_view(), name='community_advertisers'),

    re_path(r'^staff_window/(?P<pk>[0-9]+)/(?P<uuid>[0-9a-f-]+)/$', CommunityStaffWindow.as_view()),
    re_path(r'^load_include_users/(?P<pk>[0-9]+)/$', CommunityPrivateIncludeUsers.as_view()),
    re_path(r'^load_exclude_users/(?P<pk>[0-9]+)/$', CommunityPrivateExcludeUsers.as_view()),
]

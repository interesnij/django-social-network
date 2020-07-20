from django.conf.urls import url
from communities.views.manage import *


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/general/$', CommunityGeneralChange.as_view(), name='community_general_form'),

    url(r'^notify_post/(?P<pk>[0-9]+)/$', CommunityNotifyPostView.as_view(), name='community_post_notify'),
    url(r'^notify_photo/(?P<pk>[0-9]+)/$', CommunityNotifyPhotoView.as_view(), name='community_photo_notify'),
    url(r'^notify_good/(?P<pk>[0-9]+)/$', CommunityNotifyGoodView.as_view(), name='community_good_notify'),
    url(r'^notify_video/(?P<pk>[0-9]+)/$', CommunityNotifyVideoView.as_view(), name='community_video_notify'),

    url(r'^private_post/(?P<pk>[0-9]+)/$', CommunityPrivatePostView.as_view(), name='community_post_private'),
    url(r'^private_photo/(?P<pk>[0-9]+)/$', CommunityPrivatePhotoView.as_view(), name='community_photo_private'),
    url(r'^private_good/(?P<pk>[0-9]+)/$', CommunityPrivateGoodView.as_view(), name='community_good_private'),
    url(r'^private_video/(?P<pk>[0-9]+)/$', CommunityPrivateVideoView.as_view(), name='community_video_private'),

    url(r'^(?P<pk>[0-9]+)/admins/$', CommunityAdminView.as_view(), name='community_admins'),
    url(r'^(?P<pk>[0-9]+)/moders/$', CommunityModersView.as_view(), name='community_moders'),
    url(r'^(?P<pk>[0-9]+)/black_list/$', CommunityBlackListView.as_view(), name='community_black_list'),
    url(r'^(?P<pk>[0-9]+)/follows/$', CommunityFollowsView.as_view(), name='community_follows'),
    url(r'^(?P<pk>[0-9]+)/members/$', CommunityMemberManageView.as_view(), name='community_member_manage'),
    url(r'^(?P<pk>[0-9]+)/editors/$', CommunityEditorsView.as_view(), name='community_editors'),
    url(r'^(?P<pk>[0-9]+)/rekl/$', CommunityAdvertisersView.as_view(), name='community_advertisers'),

    url(r'^staff_window/(?P<pk>[0-9]+)/(?P<uuid>[0-9a-f-]+)/$', CommunityStaffWindow.as_view()),
]

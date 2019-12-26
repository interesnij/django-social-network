from django.conf.urls import url
from communities.views.manage import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/general/$', login_required(CommunityGeneralChange.as_view()), name='community_general_form'),
    url(r'^cat/(?P<pk>[0-9]+)/$', login_required(CommunityCatChange.as_view()), name='community_cat'),
    url(r'^(?P<pk>[0-9]+)/avatar/$', login_required(CommunityAvatarChange.as_view()), name='community_avatar'),
    url(r'^(?P<pk>[0-9]+)/cover/$', login_required(CommunityCoverChange.as_view()), name='community_cover'),
    url(r'^(?P<pk>[0-9]+)/settings_notify/$', login_required(CommunityNotifyView.as_view()), name='community_notify'),
    url(r'^(?P<pk>[0-9]+)/settings_private/$', login_required(CommunityPrivateView.as_view()), name='community_private'),
    url(r'^(?P<pk>[0-9]+)/admins/$', login_required(CommunityAdminView.as_view()), name='community_admins'),
    url(r'^(?P<pk>[0-9]+)/moders/$', login_required(CommunityModersView.as_view()), name='community_moders'),
    url(r'^(?P<pk>[0-9]+)/black_list/$', login_required(CommunityBlackListView.as_view()), name='community_black_list'),
    url(r'^(?P<pk>[0-9]+)/follows/$', login_required(CommunityFollowsView.as_view()), name='community_follows'),

]

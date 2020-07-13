from django.conf.urls import url
from communities.views.manage import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/general/$', login_required(CommunityGeneralChange.as_view()), name='community_general_form'),
    url(r'^cat/(?P<pk>[0-9]+)/$', login_required(CommunityCatChange.as_view()), name='community_cat'),
    url(r'^(?P<pk>[0-9]+)/notify/$', login_required(CommunityNotifyView.as_view()), name='community_notify'),
    url(r'^(?P<pk>[0-9]+)/private/$', login_required(CommunityPrivateView.as_view()), name='community_private'),

    url(r'^(?P<pk>[0-9]+)/admins/$', login_required(CommunityAdminView.as_view()), name='community_admins'),
    url(r'^(?P<pk>[0-9]+)/moders/$', login_required(CommunityModersView.as_view()), name='community_moders'),
    url(r'^(?P<pk>[0-9]+)/black_list/$', login_required(CommunityBlackListView.as_view()), name='community_black_list'),
    url(r'^(?P<pk>[0-9]+)/follows/$', login_required(CommunityFollowsView.as_view()), name='community_follows'),
    url(r'^(?P<pk>[0-9]+)/members/$', login_required(CommunityMemberManageView.as_view()), name='community_member_manage'),
    url(r'^(?P<pk>[0-9]+)/editors/$', login_required(CommunityEditorsView.as_view()), name='community_editors'),
    url(r'^(?P<pk>[0-9]+)/rekl/$', login_required(CommunityAdvertisersView.as_view()), name='community_advertisers'),

    url(r'^staff_window/(?P<pk>[0-9]+)/(?P<uuid>[0-9a-f-]+)/$', login_required(CommunityStaffWindow.as_view())),
]

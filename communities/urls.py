from django.conf.urls import url
from communities.views.list import AllCommunities, CommunitiesView, CommunityMembersView
from communities.views.details import CommunityItemView, CommunityListView, CommunityDetailView, CommunityDetailReload
from communities.views.progs import CommunityCreate, CommunitiesCatsView, GygView, CommunityMemberCreate, CommunityMemberDelete
from communities.views.manage import (
                                        CommunityGeneralChange,
                                        CommunityCatChange,
                                        CommunityAvatarChange,
                                        CommunityCoverChange,
                                        CommunityNotifyView,
                                        CommunityPrivateView,
                                        CommunityAdminView,
                                        CommunityModersView,
                                        CommunityBlackListView,
                                        CommunityFollowsView,
                                    )

urlpatterns = [
    url(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),
    url(r'^user/(?P<pk>\d+)/$', CommunitiesView.as_view(), name='communities'),
    url(r'^(?P<pk>\d+)/members/$', CommunityMembersView.as_view(), name='community_members'),

    url(r'^(?P<pk>\d+)/$', CommunityDetailView.as_view(), name='community_detail'),
    url(r'^reload/(?P<pk>\d+)/$', CommunityDetailReload.as_view(), name='community_detail_reload'),
    url(r'^item/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', CommunityItemView.as_view(), name='community_item'),
    url(r'^list/(?P<pk>\d+)/$', CommunityListView.as_view(), name="community_item_list"),

    url(r'^add/$', CommunityCreate.as_view(), name="add_community"),
    url(r'^cat/(?P<order>\d+)/$',CommunitiesCatsView.as_view(), name="communities_cats"),
    url(r'^gygyg/$', GygView.as_view(), name="community_ggg"),
    url(r'^add_community_member/(?P<pk>\d+)/$', CommunityMemberCreate.as_view(), name="add_community_member"),
    url(r'^delete_community_member/(?P<pk>\d+)/$', CommunityMemberDelete.as_view(), name="delete_community_member"),

    url(r'^general/(?P<pk>[0-9]+)/$', CommunityGeneralChange.as_view(), name='community_general_form'),
    url(r'^cat/(?P<pk>[0-9]+)/$', CommunityCatChange.as_view(), name='community_cat'),
    url(r'^avatar/(?P<pk>[0-9]+)/$', CommunityAvatarChange.as_view(), name='community_avatar'),
    url(r'^cover/(?P<pk>[0-9]+)/$', CommunityCoverChange.as_view(), name='community_cover'),
    url(r'^settings_notify/(?P<pk>[0-9]+)/$', CommunityNotifyView.as_view(), name='community_notify'),
    url(r'^settings_private/(?P<pk>[0-9]+)/$', CommunityPrivateView.as_view(), name='community_private'),
    url(r'^admins/(?P<pk>[0-9]+)/$', CommunityAdminView.as_view(), name='community_admins'),
    url(r'^moders/(?P<pk>[0-9]+)/$', CommunityModersView.as_view(), name='community_moders'),
    url(r'^black_list/(?P<pk>[0-9]+)/$', CommunityBlackListView.as_view(), name='community_black_list'),
    url(r'^follows/(?P<pk>[0-9]+)/$', CommunityFollowsView.as_view(), name='community_follows'),

]

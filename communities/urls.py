from django.urls import re_path, include
from communities.views.list import *
from communities.views.details import *


urlpatterns = [
    re_path(r'^all-communities/$', AllCommunities.as_view(), name='all_communities'),
    re_path(r'^trend-communities/$', TrendCommunities.as_view(), name='trend_communities'),
    re_path(r'^category/(?P<pk>\d+)/$', CommunityCategoryView.as_view(), name='community_category'),

    re_path(r'^members/(?P<pk>\d+)/$', CommunityMembersView.as_view(), name='community_members'),
    re_path(r'^friends/(?P<pk>\d+)/$', CommunityFriendsView.as_view(), name='community_friends'),

    re_path(r'^draft/(?P<pk>\d+)/$', PostsDraftCommunity.as_view(), name="community_draft_list"),
    re_path(r'^user_draft/(?P<pk>\d+)/$', PostsUserDraftCommunity.as_view(), name="community_user_draft_list"),

    re_path(r'^(?P<pk>\d+)/music/$', CommunityMusic.as_view(), name='community_music'),
    re_path(r'^(?P<pk>\d+)/music_list/(?P<uuid>[0-9a-f-]+)/$', CommunityMusicList.as_view(), name='community_music_list'),

    re_path(r'^(?P<pk>\d+)/video/$', CommunityVideo.as_view(), name='community_video'),
    re_path(r'^(?P<pk>\d+)/video_list/(?P<uuid>[0-9a-f-]+)/$', CommunityVideoList.as_view(), name='community_video_list'),

    re_path(r'^(?P<pk>\d+)/docs/$', CommunityDocs.as_view(), name='community_docs'),
    re_path(r'^(?P<pk>\d+)/doc_list/(?P<uuid>[0-9a-f-]+)/$', CommunityDocsList.as_view(), name='community_docs_list'),

    re_path(r'^(?P<pk>\d+)/goods/$', CommunityGoods.as_view(), name='community_goods'),
    re_path(r'^(?P<pk>\d+)/goods_list/(?P<uuid>[0-9a-f-]+)/$', CommunityGoodsList.as_view(), name='community_goods_list'),

    re_path(r'^(?P<pk>\d+)/photos/$', CommunityGallery.as_view(), name='community_gallery'),
    re_path(r'^(?P<pk>\d+)/photo_list/(?P<uuid>[0-9a-f-]+)/$', CommunityPhotoList.as_view(), name='community_photo_list'),

    re_path(r'^manage/', include('communities.url.manage')),
    re_path(r'^progs/', include('communities.url.progs')),
    re_path(r'^stat/', include('communities.url.stat')),

]

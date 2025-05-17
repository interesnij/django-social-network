from django.urls import re_path
from communities.views.progs import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    re_path(r'^add_member/(?P<pk>\d+)/$', CommunityMemberCreate.as_view()),
    re_path(r'^delete_member/(?P<pk>\d+)/$', CommunityMemberDelete.as_view()),
    re_path(r'^manager_add_member/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityManageMemberCreate.as_view()),
    re_path(r'^manager_delete_member/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityManageMemberDelete.as_view()),

    re_path(r'^add/$', CommunityCreate.as_view(), name="add_community"),
    re_path(r'^cat/(?P<order>\d+)/$',CommunitiesCatsView.as_view(), name="communities_cats"),

    re_path(r'^add_admin/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdminCreate.as_view()),
    re_path(r'^delete_admin/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdminDelete.as_view()),
    re_path(r'^add_moderator/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityModerCreate.as_view()),
    re_path(r'^delete_moderator/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityModerDelete.as_view()),
    re_path(r'^add_editor/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityEditorCreate.as_view()),
    re_path(r'^delete_editor/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityEditorDelete.as_view()),
    re_path(r'^add_advertiser/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdvertiserCreate.as_view()),
    re_path(r'^delete_advertiser/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityAdvertiserDelete.as_view()),
    re_path(r'^add_banned/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityBannedCreate.as_view()),
    re_path(r'^delete_banned/(?P<community_pk>\d+)/(?P<user_pk>\d+)/$', CommunityBannedDelete.as_view()),
]

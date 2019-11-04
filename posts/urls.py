from posts.views import (
                            PostsView,
                            PostDetailView,
                            PostUserCreate,
                            PostCommunityCreate,

                            RepostUserUser,
                            RepostUserCommunity,
                            RepostCommunityCommunity,
                            RepostCommunityUser,
                        )
from django.conf.urls import url



urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^add_post/$', PostUserCreate.as_view(), name="post_add_user"),
    url(r'^add_post_community/(?P<pk>\d+)/$', PostCommunityCreate.as_view(), name="post_add_community"),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostDetailView.as_view(), name='post_detail'),

    url(r'^repost_user_user/(?P<uuid>[0-9a-f-]+)/$', RepostUserUser.as_view(), name="repost_user_user"),
    url(r'^repost_user_community/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RepostUserCommunity.as_view(), name="repost_user_community"),
    url(r'^repost_community_community/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', RepostCommunityCommunity.as_view(), name="repost_community_community"),
    url(r'^repost_community_user/(?P<pk>\d+)/$', RepostCommunityUser.as_view(), name="repost_community_user"),
]

from posts.views import *
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^add_post/(?P<pk>\d+)/$', login_required(PostUserCreate.as_view()), name="post_add_user"),
    url(r'^add_post_community/(?P<pk>\d+)/$', login_required(PostCommunityCreate.as_view())),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostDetailView.as_view(), name='post_detail'),

    url(r'^repost_user_user/(?P<uuid>[0-9a-f-]+)/$', login_required(RepostUserUser.as_view()), name='user_user_repost'),
    url(r'^repost_user_community/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(RepostUserCommunity.as_view()), name="repost_user_community"),
    url(r'^repost_community_community/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(RepostCommunityCommunity.as_view()), name="repost_community_community"),
    url(r'^repost_community_user/(?P<pk>\d+)/$', login_required(RepostCommunityUser.as_view()), name="repost_community_user"),

    url(r'^user/', include('main.url.user')),
	url(r'^community/', include('main.url.community')),
	url(r'^votes/', include('main.url.votes')),
	url(r'^item_window/', include('main.url.window')),
]

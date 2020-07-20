from posts.views import *
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostDetailView.as_view(), name='post_detail'),

    url(r'^repost_user_user/(?P<uuid>[0-9a-f-]+)/$', login_required(RepostUserUser.as_view()), name='user_user_repost'),
    url(r'^repost_user_community/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(RepostUserCommunity.as_view()), name="repost_user_community"),
    url(r'^repost_community_community/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(RepostCommunityCommunity.as_view()), name="repost_community_community"),
    url(r'^repost_community_user/(?P<pk>\d+)/$', login_required(RepostCommunityUser.as_view()), name="repost_community_user"),

    url(r'^user/', include('posts.url.user')),
	url(r'^community/', include('posts.url.community')),
	url(r'^votes/', include('posts.url.votes')),
	url(r'^item_window/', include('posts.url.window')),
    url(r'^user_progs/', include('posts.url.user_progs')),
    url(r'^community_progs/', include('posts.url.community_progs')),
]

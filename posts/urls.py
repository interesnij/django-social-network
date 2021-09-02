from django.conf.urls import url, include
from posts.views import PostsView, LoadPostList


urlpatterns = [
    url(r'^$', PostsView.as_view()),
    url(r'^load_list/(?P<uuid>[0-9a-f-]+)/$', LoadPostList.as_view(), name="load_post_list"),

    url(r'^user/', include('posts.url.user')),
	url(r'^community/', include('posts.url.community')),
	url(r'^votes/', include('posts.url.votes')),
	url(r'^item_window/', include('posts.url.window')),
    url(r'^user_progs/', include('posts.url.user_progs')),
    url(r'^community_progs/', include('posts.url.community_progs')),
    url(r'^repost/', include('posts.url.repost')),
]

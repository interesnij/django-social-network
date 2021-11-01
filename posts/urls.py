from django.conf.urls import url, include
from posts.views import *


urlpatterns = [
    url(r'^$', PostsView.as_view()),
    url(r'^load_list/(?P<pk>\d+)/$', LoadPostsList.as_view(), name="load_post_list"),
    url(r'^post/(?P<pk>\d+)/$', LoadPost.as_view(), name="load_post"),
    url(r'^fix_post/(?P<pk>\d+)/$', LoadFixPost.as_view(), name="load_fix_post"),
    url(r'^comments/(?P<pk>\d+)/$', PostCommentList.as_view()),

    url(r'^user/', include('posts.url.user')),
	url(r'^community/', include('posts.url.community')),
	url(r'^votes/', include('posts.url.votes')),
	url(r'^item_window/', include('posts.url.window')),
    url(r'^user_progs/', include('posts.url.user_progs')),
    url(r'^community_progs/', include('posts.url.community_progs')),
    url(r'^repost/', include('posts.url.repost')),
]

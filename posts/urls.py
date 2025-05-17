from django.urls import re_path, include
from posts.views import *


urlpatterns = [
    re_path(r'^$', PostsView.as_view()),
    re_path(r'^post/(?P<pk>\d+)/$', LoadPost.as_view(), name="load_post"),
    re_path(r'^fix_post/(?P<pk>\d+)/$', LoadFixPost.as_view(), name="load_fix_post"),
    re_path(r'^list/$', LoadPostsList.as_view()),

    re_path(r'^load_include_users/(?P<pk>\d+)/$', PostListLoadIncludeUsers.as_view()),
    re_path(r'^load_exclude_users/(?P<pk>\d+)/$', PostListLoadExcludeUsers.as_view()),

    re_path(r'^user/', include('posts.url.user')),
	re_path(r'^community/', include('posts.url.community')),
    re_path(r'^user_progs/', include('posts.url.user_progs')),
    re_path(r'^community_progs/', include('posts.url.community_progs')),
]

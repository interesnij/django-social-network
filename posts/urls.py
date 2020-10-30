from posts.views import *
from django.conf.urls import url, include


urlpatterns = [
    url(r'^user/', include('posts.url.user')),
	url(r'^community/', include('posts.url.community')),
	url(r'^votes/', include('posts.url.votes')),
	url(r'^item_window/', include('posts.url.window')),
    url(r'^user_progs/', include('posts.url.user_progs')),
    url(r'^community_progs/', include('posts.url.community_progs')),
    url(r'^repost/', include('posts.url.repost')),
]

from django.conf.urls import url
from posts.view.votes import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<post_pk>\d+)/(?P<pk>\d+)/$',login_required(PostUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<post_pk>\d+)/(?P<pk>\d+)/$',login_required(PostUserDislikeCreate.as_view())),
	url(r'^community_like/(?P<post_pk>\d+)/(?P<pk>\d+)/$',login_required(PostCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<post_pk>\d+)/(?P<pk>\d+)/$',login_required(PostCommunityDislikeCreate.as_view())),
]

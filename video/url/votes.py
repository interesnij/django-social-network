from django.conf.urls import url
from video.view.votes import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<video_pk>\d+)/(?P<pk>\d+)/$',login_required(VideoUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<video_pk>\d+)/(?P<pk>\d+)/$',login_required(VideoUserDislikeCreate.as_view())),
	url(r'^community_like/(?P<video_pk>\d+)/(?P<pk>\d+)/$',login_required(VideoCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<video_pk>\d+)/(?P<pk>\d+)/$',login_required(VideoCommunityDislikeCreate.as_view())),
]

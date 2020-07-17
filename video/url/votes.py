from django.conf.urls import url
from video.view.votes import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(VideoUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(VideoUserDislikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(VideoCommentUserLikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(VideoCommentUserDislikeCreate.as_view())),

	url(r'^community_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(VideoCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(VideoCommunityDislikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(VideoCommentCommunityLikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(VideoCommentCommunityDislikeCreate.as_view())),
]

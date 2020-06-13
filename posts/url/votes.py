from django.conf.urls import url
from main.view.votes import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PostUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PostUserDislikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(PostCommentUserLikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(PostCommentUserDislikeCreate.as_view())),

	url(r'^community_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PostCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PostCommunityDislikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(PostCommentCommunityLikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(PostCommentCommunityDislikeCreate.as_view())),
]

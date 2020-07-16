from django.conf.urls import url
from goods.view.votes import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(GoodUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(GoodUserDislikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(GoodCommentUserLikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(GoodCommentUserDislikeCreate.as_view())),

	url(r'^community_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(GoodCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(GoodCommunityDislikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(GoodCommentCommunityLikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(GoodCommentCommunityDislikeCreate.as_view())),
]

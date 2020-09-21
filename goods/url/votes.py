from django.conf.urls import url
from goods.view.votes import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<good_pk>\d+)/(?P<pk>\d+)/$',login_required(GoodUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<good_pk>\d+)/(?P<pk>\d+)/$',login_required(GoodUserDislikeCreate.as_view())),
    url(r'^user_comment/(?P<good_pk>\d+)/(?P<pk>\d+)/like/$',login_required(GoodCommentUserLikeCreate.as_view())),
    url(r'^user_comment/(?P<good_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(GoodCommentUserDislikeCreate.as_view())),

	url(r'^community_like/(?P<pk>\d+)/(?P<good_pk>\d+)/$',login_required(GoodCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<pk>\d+)/(?P<good_pk>\d+)/$',login_required(GoodCommunityDislikeCreate.as_view())),
    url(r'^community_comment/(?P<pk>\d+)/(?P<good_pk>\d+)/like/$',login_required(GoodCommentCommunityLikeCreate.as_view())),
    url(r'^community_comment/(?P<pk>\d+)/(?P<good_pk>\d+)/dislike/$',login_required(GoodCommentCommunityDislikeCreate.as_view())),
]

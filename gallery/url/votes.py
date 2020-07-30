from django.conf.urls import url
from gallery.view.votes import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^user_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PhotoUserLikeCreate.as_view())),
    url(r'^user_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PhotoUserDislikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(PhotoCommentUserLikeCreate.as_view())),
    url(r'^user_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(PhotoCommentUserDislikeCreate.as_view())),

	url(r'^community_like/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PhotoCommunityLikeCreate.as_view())),
    url(r'^community_dislike/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$',login_required(PhotoCommunityDislikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/like/$',login_required(PhotoCommentCommunityLikeCreate.as_view())),
    url(r'^community_comment/(?P<comment_pk>\d+)/(?P<pk>\d+)/dislike/$',login_required(PhotoCommentCommunityDislikeCreate.as_view())),
]

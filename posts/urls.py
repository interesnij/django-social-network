from posts.views import PostsView, PostUserHardCreate, PostUserMediumCreate, PostUserLiteCreate
from django.conf.urls import url
from main.models import LikeDislike
from main.views import VotesView
from post.models import Post


urlpatterns = [
    url(r'^posts/$', PostsView.as_view(), name='posts'),
    url(r'^add_hard/$', PostUserHardCreate.as_view(), name="post_add_hard_user"),
    url(r'^add_medium/$', PostUserMediumCreate.as_view(), name="post_add_medium_user"),
    url(r'^add_lite/$', PostUserLiteCreate.as_view(), name="post_add_lite_user"),
    url(r'^like/(?P<pk>\d+)/$',login_required(
    VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)
    ),name='post_like'),
    url(r'^dislike/(?P<pk>\d+)/$',login_required(
    VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE)
    ),name='post_dislike'),
]

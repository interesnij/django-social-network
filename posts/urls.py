from posts.views import (
                            PostsView,
                            PostUserHardCreate,
                            PostUserMediumCreate,
                            PostUserLiteCreate,
                            PostDeleteView,
                            CommentCreateView,
                            PostDislikeView,
                            PostLikeView,
                            PostCommentLikeView,
                            PostCommentDislikeView,
                            update_interactions,
                            get_comment,
                            post_comment,
                            reply_comment,
                        )
from django.conf.urls import url
from main.models import LikeDislike
from main.views import VotesView
from posts.models import Post, PostComment
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^add_hard/$', PostUserHardCreate.as_view(), name="post_add_hard_user"),
    url(r'^add_medium/$', PostUserMediumCreate.as_view(), name="post_add_medium_user"),
    url(r'^add_lite/$', PostUserLiteCreate.as_view(), name="post_add_lite_user"),
    url(r'^like/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)),name='post_like'),
    url(r'^dislike/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE)),name='post_dislike'),
    url(r'^comment/(?P<pk>\d+)/like/$',login_required(VotesView.as_view(model=PostComment, vote_type=LikeDislike.LIKE)),name='post_comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',login_required(VotesView.as_view(model=PostComment, vote_type=LikeDislike.DISLIKE)),name='post_comment_dislike'),
    url(r'^delete/(?P<pk>\d+)/$', PostDeleteView.as_view(), name='delete_post'),
    url(r'^like_window/(?P<pk>\d+)/$', PostLikeView.as_view(), name='post_like_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', PostCommentLikeView.as_view(), name='post_comment_like_window'),
    url(r'^dislike_window/(?P<pk>\d+)/$', PostDislikeView.as_view(), name='post_dislike_window'),
    url(r'^comment_dislike_window/(?P<pk>\d+)/$', PostCommentDislikeView.as_view(), name='post_comment_dislike_window'),
    url(r'^get-comment/$', get_comment, name='get_comment'),
    url(r'^post-comment/$', post_comment, name='post_comments'),
    url(r'^reply-comment/$', reply_comment, name='reply_comment'),
    url(r'^update-interactions/$', update_interactions, name='update_interactions'),

]

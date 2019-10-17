from posts.views import (
                            PostsView,
                            PostDetailView,
                            PostDislikeView,
                            PostLikeView,
                            PostCommentLikeView,
                            PostUserCreate,
                            PostCommentDislikeView,
                            post_update_interactions,
                        )
from django.conf.urls import url



urlpatterns = [
    url(r'^$', PostsView.as_view(), name='posts'),
    url(r'^add_post/$', PostUserCreate.as_view(), name="post_add_user"),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostDetailView.as_view(), name='post_detail'),
    url(r'^like_window/(?P<pk>\d+)/$', PostLikeView.as_view(), name='post_like_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', PostCommentLikeView.as_view(), name='post_comment_like_window'),
    url(r'^dislike_window/(?P<pk>\d+)/$', PostDislikeView.as_view(), name='post_dislike_window'),
    url(r'^comment_dislike_window/(?P<pk>\d+)/$', PostCommentDislikeView.as_view(), name='post_comment_dislike_window'),
    url(r'^update-interactions/$', post_update_interactions, name='post_update_interactions'),
]

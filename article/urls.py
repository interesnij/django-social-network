from article.views import (
                            ArticleView,
                            ArticleUserCreate,
                            ArticleNewView,
                            ArticleDetailView,
                            ArticleCommentCreateView,
                            ArticleDislikeView,
                            ArticleLikeView,
                            ArticleCommentLikeView,
                            ArticleCommentDislikeView,
                            article_update_interactions,
                            article_get_comment,
                            article_comment,
                            article_reply_comment,
                        )
from django.conf.urls import url
from main.models import LikeDislike
from main.views import VotesView
from article.models import Article, ArticleComment


urlpatterns = [
    url(r'^$', ArticleView.as_view(), name='articles'),
    url(r'^add/$', ArticleUserCreate.as_view(), name="article_add_user"),
    url(r'^new/(?P<uuid>[0-9a-f-]+)/$', ArticleNewView.as_view(), name='article_new'),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^like_window/(?P<pk>\d+)/$', ArticleLikeView.as_view(), name='article_like_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', ArticleCommentLikeView.as_view(), name='article_comment_like_window'),
    url(r'^dislike_window/(?P<pk>\d+)/$', ArticleDislikeView.as_view(), name='article_dislike_window'),
    url(r'^comment_dislike_window/(?P<pk>\d+)/$', ArticleCommentDislikeView.as_view(), name='article_comment_dislike_window'),
    url(r'^article-comment/$', article_get_comment, name='article_get_comment'),
    url(r'^post-comment/$', article_comment, name='article_comments'),
    url(r'^reply-comment/$', article_reply_comment, name='article_reply_comment'),
    url(r'^update-interactions/$', article_update_interactions, name='article_update_interactions'),

]

from article.views import (
                            ArticleView,
                            ArticleUserHardCreate,
                            ArticleUserMediumCreate,
                            ArticleUserLiteCreate,
                            ArticleDeleteView,
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
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', ArticleView.as_view(), name='articles'),
    url(r'^add_hard/$', ArticleUserHardCreate.as_view(), name="article_add_hard_user"),
    url(r'^add_medium/$', ArticleUserMediumCreate.as_view(), name="article_add_medium_user"),
    url(r'^add_lite/$', ArticleUserLiteCreate.as_view(), name="article_add_lite_user"),
    url(r'^like/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Article, vote_type=LikeDislike.LIKE)),name='article_like'),
    url(r'^dislike/(?P<pk>\d+)/$',login_required(VotesView.as_view(model=Article, vote_type=LikeDislike.DISLIKE)),name='article_dislike'),
    url(r'^comment/(?P<pk>\d+)/like/$',login_required(VotesView.as_view(model=ArticleComment, vote_type=LikeDislike.LIKE)),name='article_comment_like'),
    url(r'^comment/(?P<pk>\d+)/dislike/$',login_required(VotesView.as_view(model=ArticleComment, vote_type=LikeDislike.DISLIKE)),name='article_comment_dislike'),
    url(r'^delete/(?P<pk>\d+)/$', ArticleDeleteView.as_view(), name='article_delete'),
    url(r'^detail/<article_id>/$', ArticleDetailView.as_view(), name='article_detail'), 
    url(r'^like_window/(?P<pk>\d+)/$', ArticleLikeView.as_view(), name='article_like_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', ArticleCommentLikeView.as_view(), name='article_comment_like_window'),
    url(r'^dislike_window/(?P<pk>\d+)/$', ArticleDislikeView.as_view(), name='article_dislike_window'),
    url(r'^comment_dislike_window/(?P<pk>\d+)/$', ArticleCommentDislikeView.as_view(), name='article_comment_dislike_window'),
    url(r'^article-comment/$', article_get_comment, name='article_get_comment'),
    url(r'^post-comment/$', article_comment, name='article_comments'),
    url(r'^reply-comment/$', article_reply_comment, name='article_reply_comment'),
    url(r'^update-interactions/$', article_update_interactions, name='article_update_interactions'),

]

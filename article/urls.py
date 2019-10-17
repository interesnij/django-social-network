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
                        )
from django.conf.urls import url


urlpatterns = [
    url(r'^$', ArticleView.as_view(), name='articles'),
    url(r'^add/$', ArticleUserCreate.as_view(), name="article_add_user"),
    url(r'^new/(?P<uuid>[0-9a-f-]+)/$', ArticleNewView.as_view(), name='article_new'),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', ArticleDetailView.as_view(), name='article_detail'),
    url(r'^like_window/(?P<pk>\d+)/$', ArticleLikeView.as_view(), name='article_like_window'),
    url(r'^comment_like_window/(?P<pk>\d+)/$', ArticleCommentLikeView.as_view(), name='article_comment_like_window'),
    url(r'^dislike_window/(?P<pk>\d+)/$', ArticleDislikeView.as_view(), name='article_dislike_window'),
    url(r'^comment_dislike_window/(?P<pk>\d+)/$', ArticleCommentDislikeView.as_view(), name='article_comment_dislike_window'),
    url(r'^update-interactions/$', article_update_interactions, name='article_update_interactions'),

]

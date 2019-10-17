from article.views import (
                            ArticleView,
                            ArticleUserCreate,
                            ArticleNewView,
                            ArticleDetailView,
                        )
from django.conf.urls import url


urlpatterns = [
    url(r'^$', ArticleView.as_view(), name='articles'),
    url(r'^add/$', ArticleUserCreate.as_view(), name="article_add_user"),
    url(r'^new/(?P<uuid>[0-9a-f-]+)/$', ArticleNewView.as_view(), name='article_new'),
    url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', ArticleDetailView.as_view(), name='article_detail'),
]

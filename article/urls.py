from article.views import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^$', ArticleView.as_view(), name='articles'),
    url(r'^add_user/(?P<pk>\d+)/$', login_required(ArticleUserCreate.as_view()), name="article_add_user"),
    url(r'^add_community/(?P<pk>\d+)/$', login_required(ArticleCommunityCreate.as_view())),
    url(r'^c_article_window/(?P<pk>\d+)/$', login_required(ArticleCommunityWindow.as_view())),
    url(r'^u_article/(?P<pk>\d+)/$', login_required(ArticleUserWindow.as_view()), name="article_user_create"),
    url(r'^new/(?P<uuid>[0-9a-f-]+)/$', ArticleNewView.as_view(), name='article_new'),
    url(r'^detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ArticleUserDetailView.as_view()),
    url(r'^read/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ArticleCommunityDetailView.as_view()),
]

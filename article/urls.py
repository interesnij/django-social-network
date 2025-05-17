from article.views import *
from django.urls import re_path
from django.contrib.auth.decorators import login_required


urlpatterns = [
    re_path(r'^add_user/(?P<pk>\d+)/$', login_required(ArticleUserCreate.as_view()), name="article_add_user"),
    re_path(r'^add_community/(?P<pk>\d+)/$', login_required(ArticleCommunityCreate.as_view())),
    re_path(r'^detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ArticleUserDetailView.as_view()),
    re_path(r'^read/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ArticleCommunityDetailView.as_view()),
]

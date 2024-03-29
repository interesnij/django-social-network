from article.views import *
from django.conf.urls import url
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^add_user/(?P<pk>\d+)/$', login_required(ArticleUserCreate.as_view()), name="article_add_user"),
    url(r'^add_community/(?P<pk>\d+)/$', login_required(ArticleCommunityCreate.as_view())),
    url(r'^detail/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ArticleUserDetailView.as_view()),
    url(r'^read/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', ArticleCommunityDetailView.as_view()),
]

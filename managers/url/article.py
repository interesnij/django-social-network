from django.conf.urls import url
from managers.view.article import *


urlpatterns = [
    url(r'^create_rejected/(?P<pk>\d+)/$', ArticleRejectedCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', ArticleUnverify.as_view()),

    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListArticleRejectedCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListArticleUnverify.as_view()),
]

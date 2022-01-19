from django.conf.urls import url
from managers.view.article import *


urlpatterns = [
    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', ArticleCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', ArticleCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', ArticleRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', ArticleClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', ArticleUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListArticleCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListArticleCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListArticleRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListArticleClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListArticleUnverify.as_view()),
]

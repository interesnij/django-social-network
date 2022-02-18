from django.conf.urls import url
from managers.view.good import *


urlpatterns = [
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', GoodCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', GoodRejectedCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', GoodUnverify.as_view()),

    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListGoodCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListGoodRejectedCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListGoodUnverify.as_view()),

    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentGoodCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentGoodRejectedCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentGoodUnverify.as_view()),
]

from django.conf.urls import url
from managers.view.photo import *


urlpatterns = [
    url(r'^create_close/(?P<uuid>[0-9a-f-]+)/$', PhotoCloseCreate.as_view()),
    url(r'^delete_close/(?P<uuid>[0-9a-f-]+)/$', PhotoCloseDelete.as_view()),
    url(r'^create_rejected/(?P<pk>\d+)/$', PhotoRejectedCreate.as_view()),
    url(r'^create_claim/(?P<uuid>[0-9a-f-]+)/$', PhotoClaimCreate.as_view()),
    url(r'^unverify/(?P<uuid>[0-9a-f-]+)/$', PhotoUnverify.as_view()),

    url(r'^list_create_close/(?P<uuid>[0-9a-f-]+)/$', ListPhotoCloseCreate.as_view()),
    url(r'^list_delete_close/(?P<uuid>[0-9a-f-]+)/$', ListPhotoCloseDelete.as_view()),
    url(r'^list_create_rejected/(?P<pk>\d+)/$', ListPhotoRejectedCreate.as_view()),
    url(r'^list_create_claim/(?P<uuid>[0-9a-f-]+)/$', ListPhotoClaimCreate.as_view()),
    url(r'^list_unverify/(?P<uuid>[0-9a-f-]+)/$', ListPhotoUnverify.as_view()),

    url(r'^comment_create_close/(?P<pk>\d+)/$', CommentPhotoCloseCreate.as_view()),
    url(r'^comment_delete_close/(?P<pk>\d+)/$', CommentPhotoCloseDelete.as_view()),
    url(r'^comment_create_rejected/(?P<pk>\d+)/$', CommentPhotoRejectedCreate.as_view()),
    url(r'^comment_create_claim/(?P<pk>\d+)/$', CommentPhotoClaimCreate.as_view()),
    url(r'^comment_unverify/(?P<pk>\d+)/$', CommentPhotoUnverify.as_view()),
]

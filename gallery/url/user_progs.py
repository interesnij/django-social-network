from gallery.view.user_progs import *
from django.conf.urls import url


urlpatterns=[
    url(r'^description/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoDescription.as_view()),
    url(r'^delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoDelete.as_view()),
    url(r'^abort_delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPhotoAbortDelete.as_view()),
    url(r'^open_comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserOpenCommentPhoto.as_view()),
    url(r'^close_comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserCloseCommentPhoto.as_view()),
    url(r'^on_private/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserOnPrivatePhoto.as_view()),
    url(r'^off_private/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserOffPrivatePhoto.as_view()),
    url(r'^add_avatar/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserAddAvatarPhoto.as_view()),
    url(r'^remove_avatar/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserRemoveAvatarPhoto.as_view()),
]

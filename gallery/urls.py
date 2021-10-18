from django.conf.urls import url, include
from gallery.views import *

urlpatterns=[
	url(r'^photo/(?P<pk>\d+)/$', PhotoDetail.as_view(), name="photo_detail"),
	url(r'^message_photo/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', MessagePhotoDetail.as_view(), name="message_photo_detail"),
	url(r'^post_photo/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', PostPhotoDetail.as_view(), name="post_photo_detail"),
	url(r'^load_list/(?P<pk>\d+)/$', LoadPhotoList.as_view(), name="load_photo_list"),

	url(r'^user/', include('gallery.url.user')),
	url(r'^community/', include('gallery.url.community')),

	url(r'^user_progs/', include('gallery.url.user_progs')),
	url(r'^community_progs/', include('gallery.url.community_progs')),

	url(r'^votes/', include('gallery.url.votes')),
	url(r'^window/', include('gallery.url.window')),
	url(r'^repost/', include('gallery.url.repost')),
]

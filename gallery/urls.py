from django.conf.urls import url, include
from gallery.views import PhotoDetail, MessagePhotoDetail

urlpatterns=[
	url(r'^photo/(?P<pk>\d+)/$', PhotoDetail.as_view(), name="photo_detail"),
	url(r'^message_photo/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', MessagePhotoDetail.as_view(), name="message_photo_detail"),

	url(r'^user/', include('gallery.url.user')),
	url(r'^community/', include('gallery.url.community')),

	url(r'^user_progs/', include('gallery.url.user_progs')),
	url(r'^community_progs/', include('gallery.url.community_progs')),

	url(r'^votes/', include('gallery.url.votes')),
	url(r'^window/', include('gallery.url.window')),
	url(r'^repost/', include('gallery.url.repost')),
]

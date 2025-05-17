from django.urls import re_path, include
from gallery.views import *

urlpatterns=[
	re_path(r'^photo/(?P<pk>\d+)/$', PhotoDetail.as_view(), name="photo_detail"),
	re_path(r'^chat_photo/(?P<pk>\d+)/(?P<photo_pk>\d+)/$', MessagePhotoDetail.as_view(), name="chat_photo"),
	re_path(r'^post_photo/(?P<post_pk>\d+)/(?P<pk>\d+)/$', PostPhotoDetail.as_view(), name="post_photo_detail"),
	re_path(r'^load_list/(?P<pk>\d+)/$', LoadPhotoList.as_view(), name="load_photo_list"),
	re_path(r'^load_list_photos/(?P<pk>\d+)/$', LoadPhotosList.as_view(), name="load_photos_list"),

	re_path(r'^add_photos_in_list/(?P<pk>\d+)/$', AddPhotosInList.as_view()),

	re_path(r'^user/', include('gallery.url.user')),
	re_path(r'^community/', include('gallery.url.community')),

	re_path(r'^user_progs/', include('gallery.url.user_progs')),
	re_path(r'^community_progs/', include('gallery.url.community_progs')),
]

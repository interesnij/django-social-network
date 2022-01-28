from gallery.view.community import *
from django.conf.urls import url

urlpatterns=[
	url(r'^list_photos/(?P<pk>\d+)/(?P<list_pk>\d+)/$', CommunityAlbumPhotosList.as_view(), name="community_photos_load"),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetCommunityPhoto.as_view()),
]

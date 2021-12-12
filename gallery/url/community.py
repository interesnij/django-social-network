from gallery.view.community import *
from django.conf.urls import url

urlpatterns=[
	url(r'^photos/(?P<pk>\d+)/$', CommunityPhotosList.as_view(), name="community_photo_list_load"),
	url(r'^preview_photo/(?P<pk>\d+)/$', GetCommunityPhoto.as_view()),
]

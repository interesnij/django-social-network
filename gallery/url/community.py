from gallery.view.community import *
from django.conf.urls import url

urlpatterns=[
	url(r'^preview_photo/(?P<pk>\d+)/$', GetCommunityPhoto.as_view()),
]

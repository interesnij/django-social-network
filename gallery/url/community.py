from gallery.view.community import *
from django.urls import re_path

urlpatterns=[
	re_path(r'^preview_photo/(?P<pk>\d+)/$', GetCommunityPhoto.as_view()),
]

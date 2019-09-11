from gallery.views import GalleryView
from django.conf.urls import url

urlpatterns=[
	url(r'^(?P<pk>\d+)/$', GalleryView.as_view(), name="gallery"),
]

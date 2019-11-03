from gallery.views import GalleryView, AlbomView
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', GalleryView.as_view(), name="gallery"),
	url(r'^img/(?P<pk>\d+)/$', AlbomView.as_view(), name="album"),
]

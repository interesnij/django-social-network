from gallery.views import GalleryView, AjaxPhotoUploadView
from django.conf.urls import url


urlpatterns=[
	url(r'^(?P<pk>\d+)/$', GalleryView.as_view(), name="gallery"),
	url(r'^(?P<pk>\d+)/ajax-upload/$', AjaxPhotoUploadView.as_view(), name="ajax_photo_upload_view"),
]

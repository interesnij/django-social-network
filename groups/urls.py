from groups.views import GrousEdit
from django.conf.urls import url

urlpatterns=[
	url(r'^(?P<pk>\d+)/$',GrousEdit.as_view(), name="groups"),
]

from django.conf.urls import url
from docs.views import DocsView


urlpatterns = [
    url(r'^$', DocsView.as_view(), name='docs'),
]

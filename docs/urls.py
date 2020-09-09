from django.conf.urls import url, include
from docs.views import DocsView


urlpatterns = [
    url(r'^$', DocsView.as_view(), name='docs'),

    url(r'^user_progs/', include('docs.url.user_progs')),
    url(r'^community_progs/', include('docs.url.community_progs')),
    url(r'^repost/', include('docs.url.repost')),
]

from django.conf.urls import url
from docs.views import DocsView


urlpatterns = [
    url(r'^$', DocsView.as_view(), name='docs'),

    url(r'^user_progs/', include('music.url.user_progs')),
    url(r'^community_progs/', include('music.url.community_progs')),
    url(r'^repost/', include('music.url.repost')),
]

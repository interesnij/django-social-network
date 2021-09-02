from django.conf.urls import url, include
from docs.views import DocsView, LoadGoodList


urlpatterns = [
    url(r'^$', DocsView.as_view()),
    url(r'^load_list/(?P<uuid>[0-9a-f-]+)/$', LoadGoodList.as_view(), name="load_good_list"),

    url(r'^user_progs/', include('docs.url.user_progs')),
    url(r'^community_progs/', include('docs.url.community_progs')),
    url(r'^repost/', include('docs.url.repost')),

    url(r'^user/', include('docs.url.user')),
    url(r'^community/', include('docs.url.community')),
]

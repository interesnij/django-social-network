from django.conf.urls import url, include
from docs.views import DocsView, LoadDocList


urlpatterns = [
    url(r'^$', DocsView.as_view()),
    url(r'^load_list/(?P<pk>\d+)/$', LoadDocList.as_view(), name="load_doc_list"),

    url(r'^user_progs/', include('docs.url.user_progs')),
    url(r'^community_progs/', include('docs.url.community_progs')),
]

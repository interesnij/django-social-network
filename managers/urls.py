from django.conf.urls import url, include
from managers.views import ManagersView


urlpatterns = [
    url(r'^$', ManagersView.as_view(), name='managers'),

    url(r'^user/', include('managers.url.user')),
    url(r'^community/', include('managers.url.community')),
    url(r'^post/', include('managers.url.post')),
    url(r'^good/', include('managers.url.good')),
    url(r'^photo/', include('managers.url.photo')),
    url(r'^video/', include('managers.url.video')),
    url(r'^audio/', include('managers.url.audio')),
]

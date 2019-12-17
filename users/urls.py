from django.conf.urls import url, include
from users.views.detail import ProfileUserView


urlpatterns = [
    url(r'^detail/', include('users.url.detail')),
    url(r'^settings/', include('users.url.settings')),
    url(r'^load/', include('users.url.load')),
    url(r'^progs/', include('users.url.progs')),
    url(r'^(?P<pk>\d+)/$', ProfileUserView.as_view(), name='user'),
]

from django.conf.urls import url, include


urlpatterns = [
    url(r'^progs/', include('users.url.progs')),
    url(r'^detail/', include('users.url.detail')),
    url(r'^settings/', include('users.url.settings')),
    url(r'^load/', include('users.url.load')),
]

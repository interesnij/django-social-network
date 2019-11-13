from django.conf.urls import url
from users.views.progs import fixed, unfixed, item_delete


urlpatterns = [
    url(r'^fixed/(?P<item_id>\d+)/$', fixed, name='fixed'),
    url(r'^unfixed/(?P<item_id>\d+)/$', unfixed, name='unfixed'),
    url(r'^delete/(?P<item_id>\d+)/$', item_delete, name='item_delete'),
]

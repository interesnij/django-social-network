from django.conf.urls import url
from follows.views import FollowsListView, FollowCreate, FollowDelete


urlpatterns = [
    url(r'^(?P<pk>\d+)/$', FollowsListView.as_view(), name='follows'),
    url(r'^add/(?P<pk>\d+)/$', FollowCreate.as_view(), name="create_follow"),
    url(r'^delete/(?P<pk>\d+)/$', FollowDelete.as_view(), name="delete_follow"),
]

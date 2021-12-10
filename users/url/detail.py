from django.conf.urls import url
from users.views.detail import *
from users.views.lists import *

urlpatterns = [
    url(r'^visit_communities/$', UserVisitCommunities.as_view(), name='visited_communities'),
    url(r'^list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UserPostsListView.as_view(), name='user_post_list'),
    url(r'^featured/$', AllFeaturedUsersList.as_view(), name='featured_users'),
]

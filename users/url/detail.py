from django.conf.urls import url
from users.views.detail import *
from users.views.lists import *

urlpatterns = [
    url(r'^post/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPostView.as_view(), name='user_post'),
    url(r'^fix_post/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserFixPostView.as_view(), name='user_fix_post'),
    url(r'^visit_communities/$', UserVisitCommunities.as_view(), name='visited_communities'),
    url(r'^list/(?P<pk>\d+)/(?P<list_pk>\d+)/$', UserPostsListView.as_view()),
    url(r'^possible/$', AllPossibleUsersList.as_view(), name='possible_users'),
]

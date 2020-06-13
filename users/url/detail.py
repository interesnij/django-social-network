from django.conf.urls import url
from users.views.detail import *
from users.views.lists import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^post/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', UserPostView.as_view(), name='user_post'),
    url(r'^visit_communities/(?P<pk>\d+)/$', UserVisitCommunities.as_view(), name='visit_communities'),
    url(r'^list/(?P<pk>\d+)/$', PostListView.as_view()),
    url(r'^possible/(?P<pk>\d+)/$', login_required(AllPossibleUsersList.as_view()), name='possible_users'),
]

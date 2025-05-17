from django.urls import re_path
from users.views.detail import *
from users.views.lists import *

urlpatterns = [
    re_path(r'^visit_communities/$', UserVisitCommunities.as_view(), name='visited_communities'),
    re_path(r'^featured_users/$', AllFeaturedUsersList.as_view(), name='featured_users'),
    re_path(r'^featured_communities/$', AllFeaturedCommunitiesList.as_view(), name='featured_communities'),
]

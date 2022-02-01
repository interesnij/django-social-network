from django.conf.urls import url
from users.views.detail import *
from users.views.lists import *

urlpatterns = [
    url(r'^visit_communities/$', UserVisitCommunities.as_view(), name='visited_communities'),
    url(r'^featured_users/$', AllFeaturedUsersList.as_view(), name='featured_users'),
    url(r'^featured_communities/$', AllFeaturedCommunitiesList.as_view(), name='featured_communities'),
]

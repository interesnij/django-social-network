from django.urls import re_path
from posts.view.community import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	re_path(r'^detail/(?P<pk>\d+)/$', PostCommunityDetail.as_view(), name="community_item_detail"),
]

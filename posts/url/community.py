from django.conf.urls import url
from posts.view.community import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^detail/(?P<pk>\d+)/$', PostCommunityDetail.as_view(), name="community_item_detail"),
]

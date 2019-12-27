from django.conf.urls import url
from main.view.community import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityCommentList.as_view()),
    url(r'^post-comment/$', login_required(ItemCommunityCommentCreate.as_view())),
    url(r'^reply-comment/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(ItemCommunityReplyCreate.as_view())),
	url(r'^fixed/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(community_fixed)),
    url(r'^unfixed/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(community_unfixed)),
    url(r'^delete/(?P<pk>\d+)/(?P<uuid>[0-9a-f-]+)/$', login_required(community_item_delete)),
	url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', ItemCommunityDetail.as_view(), name="community_item_detail"),
]

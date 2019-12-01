from django.conf.urls import url
from main.view.user import *


urlpatterns = [
	#url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommunityCommentList.as_view()),
    #url(r'^post-comment/$', item_community_post_comment),
    #url(r'^reply-comment/$', item_community_reply_comment),

	#url(r'^fixed/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', item_community_fixed),
    #url(r'^unfixed/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', item_community_unfixed),
    #url(r'^delete/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', item_community_delete),
]

from django.conf.urls import url
from main.view.user import (
							ItemCommentList,
							item_post_comment,
							item_reply_comment,
							user_fixed,
							user_unfixed,
							user_item_delete
							)


urlpatterns = [
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommentList.as_view(), name='item_get_comment'),
    url(r'^post-comment/$', item_post_comment, name='item_user_post_comment'),
    url(r'reply-comment/$', item_reply_comment, name='item_user_reply_comment'),

	url(r'^fixed/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', user_fixed, name='user_fixed'),
    url(r'^unfixed/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', user_unfixed, name='user_unfixed'),
    url(r'^delete/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', user_item_delete, name='user_item_delete'),
]

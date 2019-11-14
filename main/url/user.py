from django.conf.urls import url
from main.view.user import (
							ItemReactWindow,
							ItemCommentReactWindow,
							ItemCommentList,
							item_post_comment,
							ItemCommentReactUserCreate,
							ItemCommentReactUserDelete,
							ItemReactUserCreate,
							ItemReactUserDelete,
							item_reply_comment,
							user_fixed,
							user_unfixed,
							user_item_delete
							)


urlpatterns = [
	url(r'^react_window/(?P<pk>\d+)/$', ItemReactWindow.as_view(), name='item_react_window'),
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/$', ItemCommentList.as_view(), name='item_get_comment'),
	url(r'^comment_react/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommentReactUserCreate.as_view(), name='item_user_comment_react'),
	url(r'^comment_un_react/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommentReactUserDelete.as_view(), name='item_user_comment_un_react'),
	url(r'^react/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemReactUserCreate.as_view(), name='item_user_react'),
	url(r'^un_react/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemReactUserDelete.as_view(), name='item_user_unreact'),
    url(r'^post-comment/$', item_post_comment, name='item_user_post_comment'),
    url(r'reply-comment/$', item_reply_comment, name='item_user_reply_comment'),
	url(r'^comment_react_window/(?P<pk>\d+)/$', ItemCommentReactWindow.as_view(), name='item_comment_react_window'),

	url(r'^fixed/(?P<item_id>\d+)/$', user_fixed, name='user_fixed'),
    url(r'^unfixed/(?P<item_id>\d+)/$', user_unfixed, name='user_unfixed'),
    url(r'^delete/(?P<item_id>\d+)/$', user_item_delete, name='user_item_delete'),
]

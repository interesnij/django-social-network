from django.conf.urls import url
from main.view.user import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemUserCommentList.as_view(), name='item_get_comment'),
    url(r'^post-comment/$', login_required(item_post_comment), name='item_user_post_comment'),
    url(r'^reply-comment/$', login_required(item_reply_comment), name='item_user_reply_comment'),

	url(r'^fixed/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', login_required(user_fixed), name='user_fixed'),
    url(r'^unfixed/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', login_required(user_unfixed), name='user_unfixed'),
    url(r'^delete/(?P<pk>\d+)/(?P<user_uuid>[0-9a-f-]+)/$', login_required(user_item_delete), name='user_item_delete'),
]

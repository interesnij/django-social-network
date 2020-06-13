from django.conf.urls import url
from main.view.user import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^detail/(?P<uuid>[0-9a-f-]+)/$', PostUserDetail.as_view(), name="user_item_detail"),
	url(r'^comment/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', PostUserCommentList.as_view()),
    url(r'^post-comment/$', login_required(PostCommentUserCreate.as_view())),
    url(r'^reply-comment/$', login_required(PostReplyUserCreate.as_view())),

	url(r'^fixed/(?P<uuid>[0-9a-f-]+)/$', login_required(user_fixed)),
    url(r'^unfixed/(?P<uuid>[0-9a-f-]+)/$', login_required(user_unfixed)),
	url(r'^off_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(user_off_comment)),
    url(r'^on_comment/(?P<uuid>[0-9a-f-]+)/$', login_required(user_on_comment)),
    url(r'^delete/(?P<uuid>[0-9a-f-]+)/$', login_required(user_item_delete)),
	url(r'^abort_delete/(?P<uuid>[0-9a-f-]+)/$', login_required(user_item_abort_delete))
]

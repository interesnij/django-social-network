from django.conf.urls import url
from main.views import (
						MainPageView,
						ComingView,
						ItemReactWindow,
						ItemCommentReactWindow,
						ItemCommentList,
						NewsListView,
						item_post_comment,
						ItemCommentReactUserCreate,
						comment_un_react,
						ItemReactUserCreate,
						ItemReactUserDelete,
						item_reply_comment)
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^main/$', MainPageView.as_view(), name="main"),
	url(r'^main/react_window/(?P<pk>\d+)/$', ItemReactWindow.as_view(), name='item_react_window'),
	url(r'^main/comment/(?P<uuid>[0-9a-f-]+)/$', ItemCommentList.as_view(), name='item_get_comment'),
	url(r'^main/comment_react/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemCommentReactUserCreate.as_view(), name='item_user_comment_react'),
	url(r'^main/comment_un_react/$', item_comment_un_react, name='item_user_comment_un_react'),
	url(r'^main/react/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemReactUserCreate.as_view(), name='item_user_react'),
	url(r'^main/un_react/(?P<uuid>[0-9a-f-]+)/(?P<pk>\d+)/$', ItemReactUserDelete.as_view(), name='item_user_unreact'),
    url(r'^main/post-comment/$', item_post_comment, name='item_user_post_comment'),
    url(r'^main/reply-comment/$', item_reply_comment, name='item_user_reply_comment'),
	url(r'^main/comment_react_window/(?P<pk>\d+)/$', ItemCommentReactWindow.as_view(), name='item_comment_react_window'),
	url(r'^main/news/$', NewsListView.as_view(), name="news_list"),
]

from django.conf.urls import url
from main.views import (
						MainPageView,
						ComingView,
						ReactView,
						CommentReactView,
						get_comment,
						post_comment,
						post_comment_react,
						comment_un_react,
						post_react,
						post_unreact,
						reply_comment)
from django.contrib.auth.decorators import login_required


urlpatterns = [
	url(r'^$', ComingView.as_view(), name="coming"),
	url(r'^main/$', MainPageView.as_view(), name="main"),
	url(r'^main/react_window/(?P<pk>\d+)/$', ReactView.as_view(), name='react_window'),
	url(r'^main/comment/$', get_comment, name='get_comment'),
	url(r'^main/comment_react/$', post_comment_react, name='post_comment_react'),
	url(r'^main/comment_un_react/$', comment_un_react, name='comment_un_react'),
	url(r'^main/react/$', post_react, name='post_react'),
	url(r'^main/un_react/$', un_react, name='un_react'),
    url(r'^main/post-comment/$', post_comment, name='post_comment'),
    url(r'^main/reply-comment/$', reply_comment, name='reply_comment'),
	url(r'^main/comment_react_window/(?P<pk>\d+)/$', CommentReactView.as_view(), name='comment_react_window'),
]

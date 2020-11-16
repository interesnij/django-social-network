from django.conf.urls import url
from main.view.comments import *


urlpatterns = [
    url(r'^posts/$', PostCommentsListView.as_view(), name="post_comments_list"),
	url(r'^photos/$', PhotoCommentsListView.as_view(), name="photo_comments_list"),
	url(r'^goods/$', GoodCommentsListView.as_view(), name="good_comments_list"),
	url(r'^video/$', VideoCommentsListView.as_view(), name="video_comments_list"),
]

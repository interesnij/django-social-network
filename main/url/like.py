from django.conf.urls import url
from main.view.like import *


urlpatterns = [
    url(r'^posts/$', PostLikesListView.as_view(), name="post_likes_list"),
	url(r'^photos/$', PhotoLikesListView.as_view(), name="photo_likes_list"),
	url(r'^goods/$', GoodLikesListView.as_view(), name="good_likes_list"),
	url(r'^video/$', VideoLikesListView.as_view(), name="video_likes_list"),
]
